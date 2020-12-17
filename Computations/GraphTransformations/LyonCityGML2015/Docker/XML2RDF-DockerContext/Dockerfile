FROM python:3.8-buster

RUN apt-get update && apt-get install -q -y git \
	&& pip install rdflib \
	&& pip install lxml \
	&& pip install requests \
	&& git clone https://github.com/VCityTeam/UD-Graph.git \
	&& chmod +x ./UD-Graph/Transformations/XML-to-RDF/OWL-based-transformations/CityGML2RDF.py 

WORKDIR /

ENTRYPOINT ["python", "UD-Graph/Transformations/XML-to-RDF/OWL-based-transformations/CityGML2RDF.py"]