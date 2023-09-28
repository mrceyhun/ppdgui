# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
# Description : DQM meta store tests
# """
# import os
# import subprocess
# from backend.client.dqm_meta_client import DqmMetaStoreClient

# test_data_last_run_in_DQMGUI_data = 365755
# test_data_last_run_root_files = [
#     'backend/tests/data/DQMGUI_data/Run2023//HLTPhysics/0003657xx/DQM_V0001_R000365755__HLTPhysics__Run2023A-PromptReco-v1__DQMIO.root']


# def test_dqm_meta_eos_grinder_and_client(config_test):
#     """Test dqm_meta.eos_grinder"""
#     # --- Using confi_test yaml file, run eos_grinder to create JSON DQM meta store file. FAST_API_CONF en var is set in conftest.py
#     r = subprocess.run(["python", "backend/dqm_meta/eos_grinder.py"], shell=True)

#     # Check script run successfully
#     assert r.returncode == 0

#     # --- Read temporary find command results file and count its lines to match it with the actual ROOT file count in test directory
#     # To understand what is going on, run `tree backend/tests/data/DQMGUI_data/` command
#     with open(config_test.dqm_meta_store.find_tmp_results_file) as f:
#         find_tmp_results_line_cnt = len(f.readlines())

#     base_eos_dir = config_test.dqm_meta_store.base_dqm_eos_dir
#     run_year_dir = os.path.join(base_eos_dir, os.listdir(base_eos_dir)[0])
#     detector_dir = os.path.join(run_year_dir, os.listdir(run_year_dir)[0])
#     run_dir = os.path.join(detector_dir, os.listdir(detector_dir)[0])
#     assert len(os.listdir(run_dir)) == find_tmp_results_line_cnt

#     # --- Test DqmMetaStoreClient
#     store_client = DqmMetaStoreClient(config=config_test)

#     assert store_client.get_last_run() == test_data_last_run_in_DQMGUI_data
#     assert store_client.get_last_run_root_files() == test_data_last_run_root_files
