FROM python:3.7.0-stretch
LABEL maintainer=Florian.Mayer@dbca.wa.gov.au
LABEL description="Python 3.7.0-stretch plus Latex, GDAL and LDAP."

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install --yes \
  -o Acquire::Retries=10 --no-install-recommends \
    texlive-full lmodern libmagic-dev libproj-dev gdal-bin \
    python-dev libsasl2-dev libldap2-dev python-enchant \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements/dev.txt
RUN python manage.py collectstatic --clear --noinput -l
EXPOSE 8220
CMD ["gunicorn", "config.wsgi", "--config", "config/gunicorn.ini"]
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "-q", "-O", "-", "http://localhost:8220/healthcheck"]