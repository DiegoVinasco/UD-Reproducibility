import os
import sys
import logging
import shutil
from docker_shapechange import DockerShapechange
from demo_download_file import DemoDownloadFile

if __name__ == "__main__":
    log_filename = os.path.join(os.getcwd(), 'run_citygml3_workflow.log')

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    shapechange_input_dir = 'data/shapechange_input'
    shapechange_output_dir = 'data/shapechange_output'
    xml2rdf_input_dir = 'data/xml2rdf_input'
    xml2rdf_output_dir = 'data/xml2rdf_output'
    citygml_filename_uri = 'https://raw.githubusercontent.com/opengeospatial/CityGML-3.0Encodings/master/CityGML/Examples/_Archive/FZK-Haus_CityGML3.0_LOD3_with_ConstructiveElements_from_IFC.gml'
    citygml_filename = 'CityGML_3.0_Conceptual_Model.xml'
    conceptual_model_uml_filename = 'CityGML_3.0_Conceptual_Model.xml'
    shapechange_config_filename = 'CityGML3.0_config.xml'

    ### Download/setup dataset and conceptual models ###
    download = DemoDownloadFile(shapechange_input_dir, citygml_filename)
    download.download_file(citygml_filename_uri)
    if not os.path.isdir(shapechange_output_dir):
        os.makedirs(shapechange_output_dir)
    # download = DemoDownloadFile(xml2rdf_input_dir, citygml_filename)
    # download.download_file(citygml_filename_uri)
    full_conceptual_model_uml_src = os.path.join('../',
                                                 conceptual_model_uml_filename)
    full_conceptual_model_uml_dest = os.path.join(shapechange_input_dir,
                                                  conceptual_model_uml_filename)
    shutil.copyfile(full_conceptual_model_uml_src,
                    full_conceptual_model_uml_dest)
    full_shapechange_conf_src = os.path.join('../', shapechange_config_filename)
    full_shapechange_conf_dest = os.path.join(shapechange_input_dir,
                                              shapechange_config_filename)
    shutil.copyfile(full_shapechange_conf_src,
                    full_shapechange_conf_dest)

    ### Transform CityGML 3.0 conceptual model to UML ###
    DockerShapechange.transform_single_file(shapechange_input_dir,
                                            shapechange_output_dir,
                                            conceptual_model_uml_filename,
                                            'CityGML_3.0_ontology',
                                            shapechange_config_filename)

    ### Align CityGML ontologies
    # TODO: add ontology alignment stage to calculation

    ### Transform CityGML dataset into RDF
    # TODO: add xml2rdf stage to calculation