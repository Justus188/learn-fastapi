Setup
- Switch vsc to cmd to allow conda to work
- Remember to cd to the correct root directory

Virtual environment
- Create: Conda: `conda create --name venv_name --file requirments.txt` or just package=version
- Activate: Conda: `activate venv_name`, pip-venv: `venv_name\Scripts\activate`
- Install packages: `conda install pkgname` or `conda install -c conda-forge pkgname`
- Export:
    - Pip: requirements.txt: `pip list --format=freeze > requirements.txt`
    - Conda: env.yml: `conda env export --from-history > env.yml`

Fastapi
- Install: `conda install -c conda-forge fastapi`
- Run server: `uvicorn main:app --reload`

Alembic - DB version control
- Checks `models.Base` for changes to cached DB structure, generates "versions" which function as diffs to up/downgrade
- Note: config was done in `env.py`, not `alembic.ini`
- Create version: `alembic revision -m version_name`
- Upgrade (version can use unique string or relative indexes, latest = "head"): `alembic upgrade version`
- Downgrade: `alembic downgrade version`

Docker
- Remember to start docker desktop before doing anything
- Build image (current directory = .): `docker build -t image_name directory`
- Start container: `docker run -d --name container_name -p host_port:container_port image_name`
- List containers: `docker ps -q`
- Kill container: `docker kill container_name`
- Remove container after force-stopping: `docker rm -f container_name`
- Remove all stopped containers: `docker system prune`

Security
- Generate random secret key: `openssl rand -hex 32`