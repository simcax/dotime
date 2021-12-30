ALTER TABLE soc.ln_timemeetgo DROP CONSTRAINT fk_activitesuuid_ref_users;
ALTER TABLE soc.ln_timemeetgo DROP CONSTRAINT fk_timedmeetgouuid_ref_users;
ALTER TABLE soc.ln_timemeetgo ADD CONSTRAINT fk_activitesuuid_ref_users FOREIGN KEY (timedmeetgouuid) REFERENCES soc.timedmeetgo (timedmeetgouuid) ON DELETE CASCADE;
ALTER TABLE soc.ln_timemeetgo ADD CONSTRAINT fk_timedmeetgouuid_ref_users FOREIGN KEY (activitesuuid) REFERENCES soc.activites (activitesuuid) ON DELETE CASCADE;