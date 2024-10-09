"""Module handling time registration"""

from uuid import UUID
from time import strftime, gmtime
from datetime import datetime, timedelta
from flask import current_app, flash
from psycopg2 import DatabaseError, sql
from psycopg2.extras import DictCursor
from dotime.db import database
from dotime.profile.settings import SettingsHandling
from dotime.utils import date_utils


class TimeRegistration:
    """Class for time registration"""

    def __init__(self, userid) -> None:
        self.userid = userid

    def add_activity(self, activity_name):
        """Adds an activity to the activity table"""
        activity_uuid = False
        try:
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    INSERT INTO soc.activites (usersId,activityname)
                    VALUES ({userid},{activity_name}) RETURNING activitesuuid
                """).format(
                    userid=sql.Literal(self.userid),
                    activity_name=sql.Literal(activity_name),
                )
                cur.execute(stmt)
                activity_uuid = cur.fetchone()[0]
                conn.commit()
        except DatabaseError as error:
            print(f"Error with sql - {error}")
        finally:
            # Close connection
            conn.close()
        return activity_uuid

    def is_activityuuid(self, activity_uuid):
        """
        Takes an activity_uuid and looks it up in the database. If the uuid exists for
        the user, true is returned, otherwise false
        """
        is_activity_uuid = False
        if len(str(activity_uuid)) == 36:
            try:
                UUID(str(activity_uuid))
                try:
                    db_obj = database.Database()
                    conn = db_obj.connect()
                    with conn.cursor() as cur:
                        stmt = sql.SQL("""
                                SELECT 1 FROM soc.activites
                                WHERE usersid = {userid}
                                AND activitesuuid = {activity_uuid}
                            """).format(
                            userid=sql.Literal(self.userid),
                            activity_uuid=sql.Literal(activity_uuid),
                        )
                        cur.execute(stmt)
                        is_activity_uuid = bool(cur.rowcount)
                except DatabaseError as error:
                    current_app.logger.error("Error executing sql - error: %s", error)
                finally:
                    conn.close()
            except ValueError:
                is_activity_uuid = False

        return is_activity_uuid

    def get_activites(self, activity_name=None, activity_uuid=None):
        """Gets a list of unique activites from the database for the current user"""
        activities = {}
        try:
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor(cursor_factory=DictCursor) as cur:
                if activity_name:
                    activity_name = activity_name.strip("'")
                    activity_name = f"%{activity_name}%"
                    stmt = sql.SQL("""
                        SELECT activitesuuid, activityname FROM soc.activites
                        WHERE usersId = {userid} and activityname LIKE {activity_name}
                    """).format(
                        userid=sql.Literal(self.userid),
                        activity_name=sql.Literal(f"{activity_name}"),
                    )
                elif activity_uuid:
                    activity_uuid = activity_uuid.strip("'")
                    stmt = sql.SQL("""
                        SELECT activitesuuid, activityname FROM soc.activites
                        WHERE usersId = {userid} and activitesuuid = {activity_uuid}
                    """).format(
                        userid=sql.Literal(self.userid),
                        activity_uuid=sql.Literal(f"{activity_uuid}"),
                    )
                else:
                    stmt = sql.SQL("""
                        SELECT activitesuuid, activityname FROM soc.activites
                        WHERE usersId = {userid}
                    """).format(userid=sql.Literal(self.userid))
                cur.execute(stmt)
                current_app.logger.debug(stmt.as_string(conn))
                if cur.rowcount:
                    activities = cur.fetchall()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql - error: %s", error)
        finally:
            conn.close()
        return activities

    @classmethod
    def create_select2_data_structure_for_ajax_call(cls, data, no_list=False):
        """Creates the correct data structure for the select2 dropdown ajax call"""
        item_list = {}
        results = []
        if no_list:
            item_list = {"id": data[0][0], "text": data[0][1]}
        else:
            for uuid, activity_name in data:
                results_dict = {}
                results_dict["id"] = uuid
                results_dict["text"] = activity_name
                results.append(results_dict)

            item_list["results"] = results
        return item_list

    def add_timeregistration(
        self, activity_uuid, date, timefrom, timeto, testing=False
    ):
        # Disabling too many arguments, as we are not able to bring it down right now
        # pylint: disable=too-many-arguments
        """Adds a row to the time registration table with a link record to an activity uuid"""
        # datetime.datetime.strptime(timefrom, format)
        timereg_added = False
        if timefrom < timeto:
            timefrom_full = f"{date} {timefrom}"
            timeto_full = f"{date} {timeto}"

            if self.timestamp_is_not_registered(
                timefrom_full
            ) and self.timestamp_is_not_registered(timeto_full):
                try:
                    db_obj = database.Database()
                    conn = db_obj.connect()
                    with conn.cursor() as cur:
                        stmt = sql.SQL("""
                            INSERT INTO soc.timedmeetgo (timefrom, timeto, usersId)
                            VALUES ({timefrom_full},{timeto_full},{userid})
                            RETURNING timedmeetgouuid
                        """).format(
                            timefrom_full=sql.Literal(timefrom_full),
                            timeto_full=sql.Literal(timeto_full),
                            userid=sql.Literal(self.userid),
                        )
                        cur.execute(stmt)
                        timed_meet_go_uuid = cur.fetchone()[0]

                        stmt = sql.SQL("""
                            INSERT INTO soc.ln_timemeetgo (timedmeetgouuid,activitesuuid)
                            VALUES ({timed_meet_go_uuid},{activity_uuid})
                        """).format(
                            timed_meet_go_uuid=sql.Literal(timed_meet_go_uuid),
                            activity_uuid=sql.Literal(activity_uuid),
                        )
                        cur.execute(stmt)
                        if cur.rowcount == 1:
                            conn.commit()
                            timereg_added = True
                        else:
                            timereg_added = False
                except DatabaseError as error:
                    print(f"Error with sql {error}")
                finally:
                    conn.close()
            else:
                if not testing:
                    flash(
                        f"Time period ({timefrom_full} or {timeto_full}) is already registered."
                    )
                timereg_added = False
        else:
            if not testing:
                flash(f"Time from {timefrom} is after time to {timeto}")
            timereg_added = False
        return timereg_added

    def timestamp_is_not_registered(self, timestamp):
        """
        Check if an existing registration exists,
        where the timeperiod would overlap with the given one
        Returns TRUE if the timestamp given does not exist for the user uuid
        """
        try:
            timestamp_is_not_here = True
            db_obj = database.Database()
            conn = db_obj.connect()
            stmt = sql.SQL("""
                SELECT 1 FROM soc.timedmeetgo WHERE timefrom <= {timestamp}
                AND timeto > {timestamp} AND usersid = {userid}
            """).format(
                timestamp=sql.Literal(timestamp), userid=sql.Literal(self.userid)
            )
            with conn.cursor() as cur:
                cur.execute(stmt)
                timestamp_is_not_here = bool(cur.rowcount == 0)
                if not timestamp_is_not_here:
                    current_app.logger.debug(
                        "Rows: %s - Timestamp %s existed already. SQL :%s",
                        cur.rowcount,
                        timestamp,
                        stmt,
                    )
        except DatabaseError as error:
            print(f"Error executing SQL {stmt} - {error}")
        finally:
            conn.close()
        return timestamp_is_not_here

    def get_registrations(self, registration_date):
        """
        Get all timeregistration for a given date
        """
        try:
            rows = False
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    SELECT experimental_strftime( t.timefrom,'%H:%M') as timefrom,
                    experimental_strftime(t.timeto,'%H:%M') as timeto,
                    a.activitesuuid, a.activityname
                    FROM soc.timedmeetgo t
                    INNER JOIN soc.ln_timemeetgo l ON t.timedmeetgouuid = l.timedmeetgouuid
                    INNER JOIN soc.activites a ON l.activitesuuid = a.activitesuuid
                    WHERE t.usersId = {userid}
                    AND t.timefrom BETWEEN {registration_date_with_time_start} AND {registration_date_with_time_end}
                    ORDER BY t.timefrom
                """).format(
                    userid=sql.Literal(self.userid),
                    registration_date_with_time_start=sql.Literal(
                        f"{registration_date} 00:00:00"
                    ),
                    registration_date_with_time_end=sql.Literal(
                        f"{registration_date} 23:59:59"
                    ),
                )
                cur.execute(stmt)
                rows = cur.fetchall()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", stmt, error)
        finally:
            conn.close()
        return rows

    def get_registration_time_on_day(self, the_date):
        """
        Get the amount of time registered on a given date
        """
        try:
            time_string = "00:00"
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    SELECT AGE(MAX(t.timeto), MIN(t.timefrom) ) as timediff
                    FROM soc.users u INNER JOIN  soc.timedmeetgo t on u.usersid = t.usersid
                    WHERE u.usersid = {userid}
                    AND (t.timefrom BETWEEN {the_date_start} AND {the_date_end})
                """).format(
                    userid=sql.Literal(self.userid),
                    the_date_start=sql.Literal(f"{the_date} 00:00:00"),
                    the_date_end=sql.Literal(f"{the_date} 23:59:59"),
                )
                cur.execute(stmt)
                if cur.rowcount:
                    result = cur.fetchone()[0]
                    if result is not None:
                        time_string = strftime("%H:%M", gmtime(result.seconds))
                    else:
                        time_string = "00:00"
                else:
                    time_string = "00:00"
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", stmt, error)
        finally:
            conn.close()
        return time_string

    def get_registration_time_for_week(self, the_date):
        # Disabling unused variable since we can't get rid of return of end of week
        # pylint: disable=unused-variable
        """
        Get the amount of time registered for the week based on a given date in that week
        """
        date_util = date_utils.DoTimeDataHelp()
        start_of_week, end_of_week = date_util.get_start_end_of_week(the_date)
        hours = 0
        minutes = 0
        # Get Number of hours and minutes worked each day
        base_date = datetime.strptime(start_of_week, "%Y-%m-%d")
        for i in range(0, 6):
            this_day = base_date + timedelta(days=i)
            time_registered = self.get_registration_time_on_day(
                this_day.strftime("%Y-%m-%d")
            )
            hours += int(time_registered.split(":")[0])
            minutes += int(time_registered.split(":")[1])
        if minutes > 60:
            min_to_hours, min_to_remaining_minutes = date_util.convert_minutes_to_hours(
                minutes
            )
            hours = hours + min_to_hours
            minutes = min_to_remaining_minutes
        time_string = f"{hours:02d}:{minutes:02d}"
        return time_string

    def percentage_worked(self, user_id, date_of_any_day_in_week, input_type):
        # Disabling unused-variable since we can't get rid of last_day_of_week
        # pylint: disable=unused-variable
        """
        Returns the percentage of worked hours for a user
        for the day or week with the given date
        """
        date_util_obj = date_utils.DoTimeDataHelp()
        settings = SettingsHandling()
        worked_time = 0
        if input_type == "week":
            first_day_of_week, last_day_of_week = date_util_obj.get_start_end_of_week(
                date_of_any_day_in_week
            )
            # Retrieve number of hours worked this week so far
            worked_time = self.get_registration_time_for_week(first_day_of_week)
            # How many hours is standard for a week
            intended_time = settings.get_number_of_work_hours_for_a_week(user_id)
        elif input_type == "day":
            worked_time = self.get_registration_time_on_day(date_of_any_day_in_week)
            weekday_lengths = settings.get_workweek_day_lengths(user_id)
            daynumber = datetime.strptime(date_of_any_day_in_week, "%Y-%m-%d").weekday()
            weekday_length_hour = weekday_lengths.get(f"workdayLength{daynumber+1}Hour")
            weekday_length_minutes = weekday_lengths.get(
                f"workdayLength{daynumber+1}Minutes"
            )
            if weekday_length_hour:
                intended_time = (
                    f"{int(weekday_length_hour):02d}:{int(weekday_length_minutes):02d}"
                )
            else:
                intended_time = "00:00"
        if worked_time != "00:00":
            percentage_worked = (
                date_util_obj.convert_hours_and_minutes_to_minutes(worked_time)
                / date_util_obj.convert_hours_and_minutes_to_minutes(intended_time)
                * 100
            )
        else:
            percentage_worked = 0
        return int(percentage_worked)
