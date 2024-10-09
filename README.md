![code coverage](https://github.com/simcax/dotime/blob/master/coverage.svg)
![Lint and Build](https://github.com/simcax/dotime/actions/workflows/pylint.yml/badge.svg)
# dotime - a time registration project

My workplace is discontinuing their timeregistration application. So I decided to try and create my own, with a Python Flask project backed by [cockroachdb](https://www.cockroachlabs.com/). 

The test website is currently exposed on: https://www.dotime.me and is in a very early stage. All the groundwork is just about done. Now I am in the process of adding real functionality, starting with registration of users and login. 

I am using this oppertunity to dive into TDD and automated testing. The goal is to attain high test coverage, and test all manner of things. 

The list here is a start of what I'd like to end up with CI/CD, and how far I am:

### Completed - CI (Github Actions)
* Test all code --> Done with pytest
* Do test coverage --> Done with "coverage"
* Database migration --> Done with Flyway
* Build docker image --> Done with Github Actions
* Test Session management in redis

### Completed - CD (ArgoCD)
* Do Continuous Deployment --> Done with ArgoCD

### Future - CI
* Selenium tests

### Future - CD
* Automatic promotion from DEV --> TEST
* Automatic promotion from TEST --> PROD

### Database layout 
The database layout is now available in the code, thanks to [DbSchema](https://dbschema.com)
![layout](https://github.com/simcax/dotime/blob/master/database/layout/MainLayout.svg "Database relations")
