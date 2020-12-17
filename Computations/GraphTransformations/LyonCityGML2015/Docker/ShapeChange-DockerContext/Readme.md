## To build image
```
docker build -t liris/shapechange . 
```

## To execute transformation
```
docker run -v "$(pwd)"/data-io:/data-io liris/shapechange /data-io/CityGML2.0_config.xml
```
To use a custom shapechange configuration file replace the last argument with a path to a configuration file within a mounted folder. Note that the configuration file must point shapechange towards a valid input model located in the mounted input folder.
```
docker run -v [path to input folder]:/data-io liris/shapechange [path to configuration file]
```

**Tip!** When using a custom shapechange configuration file, be sure to specify the output directory as the mounted drive, for example:
```
<targetParameter name="outputDirectory" value="/data-io/output/"/>
```