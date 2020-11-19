FROM python:3.8-buster

RUN set -ex \
    && git clone https://github.com/VCityTeam/UD-Graph.git \
    && git checkout shapechange-integration
    && cd UD-Graph/Transformations/XML-to-RDF/XSD-based-transformations/ \
    && pip install lxml \

WORKDIR UD-Graph/Transformations/XML-to-RDF/XSD-based-transformations/
 