import sys
import logging
import time
from demo_lyon_metropole_dowload_and_sanitize_temporal \
  import DemoLyonMetropoleDowloadAndSanitizeTemporal
from demo_split_buildings_temporal import DemoSplitBuildingsTemporal
from demo_strip_attributes_temporal import DemoStripTemporal
from demo_extract_building_dates import DemoExtractBuildingDates
from demo_load_3dcitydb_temporal import DemoLoad3DCityDBTemporal
from demo_tiler_temporal import DemoTilerTemporal
from demo_3dcitydb_server_temporal import Demo3dCityDBServerTemporal

# Definition of the workflow by defining its nodes and connections
demo_download = DemoLyonMetropoleDowloadAndSanitizeTemporal('BATI', 'stage_1')

demo_split = DemoSplitBuildingsTemporal()
demo_split.set_results_dir('stage_2') 
demo_split.set_input_demo(demo_download)

demo_strip = DemoStripTemporal()
demo_strip.set_results_dir('stage_3') 
demo_strip.set_input_demo(demo_split)

demo_extract = DemoExtractBuildingDates()
demo_extract.set_results_dir('stage_4') 
demo_extract.set_input_demo(demo_strip)

demo_db_servers = Demo3dCityDBServerTemporal()

demo_load = DemoLoad3DCityDBTemporal()
demo_load.set_results_dir('stage_5') 
demo_load.set_input_demo(demo_strip)

demo_tiler = DemoTilerTemporal()
demo_tiler.set_results_dir('stage_6') 
demo_tiler.set_input_demo(demo_extract)
