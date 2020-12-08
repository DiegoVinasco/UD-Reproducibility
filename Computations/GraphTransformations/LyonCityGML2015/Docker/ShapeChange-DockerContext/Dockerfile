FROM python:3.8-buster

RUN apt-get update && apt-get install -q -y \
	openjdk-11-jdk \
	git \
	&& git clone https://github.com/VCityTeam/UD-Graph.git \
	&& chmod +x ./UD-Graph/Transformations/UML-to-OWL/run.py

WORKDIR UD-Graph/Transformations/UML-to-OWL/

VOLUME["/data"]

ENTRYPOINT ["python", "./run.py"]
CMD ["./CityGML2.0_config.xml"]