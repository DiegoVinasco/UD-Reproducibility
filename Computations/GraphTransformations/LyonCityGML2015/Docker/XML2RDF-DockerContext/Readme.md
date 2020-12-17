## To build image
```
docker build -t liris/xml2rdf . 
```

## To execute transformation
```
docker run -v "$(pwd)"/data-io:/data-io liris/xml2rdf /data-io/input/CityGML_2.0_Conceptual_Model,http://www.opengis.net/ont/geosparql#,http://www.opengis.net/ont/gml# data-io/input/LYON_1ER_BATI_2015-1_bldg.gml /data-io/output/
```
To use multiple ontologies, separate each ontology path with a comma ','. Note that http addresses can be given to import online ontologies.
```
docker run -v [path to input folder]:/data-io liris/xml2rdf [comma separated ontology paths/urls] [input file] [output path]
```
