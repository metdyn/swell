# (C) Copyright 2021- United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.


# --------------------------------------------------------------------------------------------------


import os

from swell.tasks.base.task_base import taskBase
from swell.utilities.build import build_and_source_dirs, link_path


# --------------------------------------------------------------------------------------------------


class BuildGeosByLinking(taskBase):

    def execute(self) -> None:

        # Get the experiment/geos directory
        # ---------------------------------
        swell_exp_path = self.experiment_path()
        geos_gcm_path = os.path.join(swell_exp_path, 'GEOSgcm')

        # Get paths to build and source
        # -----------------------------
        geos_gcm_build_path, geos_gcm_source_path = build_and_source_dirs(geos_gcm_path)

        # Choice to link to existing build or build GEOS
        # ----------------------------------------------
        if not self.config.geos_build_method() == 'use_existing':
            self.logger.abort(f'Found \'{self.config.geos_build_method()}\' for ' +
                              f'geos_build_method in the experiment dictionary. Must be ' +
                              f'\'use_existing\'.')

        # Assert that the existing build directory contains a bin directory
        if not os.path.exists(os.path.join(self.config.existing_geos_gcm_build_path(), 'bin')):
            self.logger.abort(f'Existing GEOS build directory is provided but a bin ' +
                              f'directory is not found in the path ' +
                              f'\'{self.config.existing_geos_gcm_build_path()}\'')

        # Write warning to user
        self.logger.info('Suitable GEOS build found, linking build directory. Warning: ' +
                         'problems will follow if the loaded modules are not consistent ' +
                         'with those used to build this version of GEOS. Also note that ' +
                         'this experiment may not be reproducible if the build changes.')

        # Link the source code directory
        link_path(self.config.existing_geos_gcm_build_path(), geos_gcm_build_path)


# --------------------------------------------------------------------------------------------------
