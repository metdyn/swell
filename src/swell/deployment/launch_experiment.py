# (C) Copyright 2021- United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

# --------------------------------------------------------------------------------------------------


# standard imports
import os

# local imports
from swell.utilities.logger import Logger
from swell.utilities.shell_commands import run_subprocess

# --------------------------------------------------------------------------------------------------


class DeployWorkflow():

    def __init__(
        self,
        suite_path: str,
        experiment_name: str,
        no_detach: bool,
        log_path: str
    ) -> None:

        self.logger = Logger('DeployWorkflow')
        self.suite_path = suite_path
        self.experiment_name = experiment_name
        self.no_detach = no_detach
        self.log_path = log_path

    # ----------------------------------------------------------------------------------------------

    def cylc_run_experiment(self) -> None:  # NB: Could be a factory based on workflow_manager

        # Move to the suite path
        os.chdir(self.suite_path)

        # Check flow.cylc is present in the provided suite path
        flow_path = os.path.join(self.suite_path, 'flow.cylc')
        if not os.path.exists(flow_path):
            self.logger.abort('In cylc_run_experiment the suite_path contains no flow.cylc file. ' +
                              'i.e. ' + flow_path + ' does not exist')

        # Check for user provided global.cylc
        if os.path.exists(self.suite_path + 'global.cylc'):
            os.environ['CYLC_CONF_PATH'] = self.suite_path

        # Install the suite
        if self.log_path:
            # Add optional path for workflow engine logging.
            option = '--symlink-dirs=run=' + self.log_path
            print(['cylc', 'install', option])
            run_subprocess(self.logger, ['cylc', 'install', option])
        else:
            run_subprocess(self.logger, ['cylc', 'install'])

        # Start the workflow

        if self.no_detach:

            # Start the suite and wait for the workflow to complete.
            run_subprocess(self.logger, ['cylc', 'play', '--no-detach', self.experiment_name])

        else:

            # Start the suite and return
            run_subprocess(self.logger, ['cylc', 'play', self.experiment_name])

            # Pre TUI messages
            self.logger.info(' ', False)
            self.logger.info('Workflow is now running... ')
            self.logger.info(' ', False)
            self.logger.info('Use \'\u001b[32mcylc scan\033[0m\' to see running workflows.')
            self.logger.info(' ', False)
            self.logger.info('If the workflow needs to be stopped, close the TUI (if open)')
            self.logger.info('by pressing \'q\' and issue either:')
            self.logger.info(' ', False)
            self.logger.info('  \u001b[32mcylc stop ' + self.experiment_name + '\033[0m')
            self.logger.info(' ', False)
            self.logger.info('or to kill running tasks and stop:')
            self.logger.info(' ', False)
            self.logger.info('  \u001b[32mcylc stop --kill ' + self.experiment_name + '\033[0m')
            self.logger.info(' ', False)

            # Launch the job monitor
            self.logger.input('Launching the TUI, press \'q\' at any time to exit the TUI')
            self.logger.info(' ', False)
            self.logger.info('TUI can be relaunched with:')
            self.logger.info(' ', False)
            self.logger.info('  \u001b[32mcylc tui ' + self.experiment_name + '\033[0m')
            self.logger.info(' ', False)
            run_subprocess(self.logger, ['cylc', 'tui', self.experiment_name])

# --------------------------------------------------------------------------------------------------


def launch_experiment(
    suite_path: str,
    no_detach: bool,
    log_path: str
) -> None:

    # Get the path to where the suite files are located
    # -------------------------------------------------
    if suite_path is None:
        suite_path = os.getcwd()
    else:
        suite_path = os.path.realpath(suite_path)  # Full absolute path

    # Get suite name
    # --------------
    experiment_name = os.path.basename(os.path.normpath(suite_path))

    # Create the deployment object
    # ----------------------------
    deploy_workflow = DeployWorkflow(suite_path, experiment_name, no_detach, log_path)

    # Write some info for the user
    # ----------------------------
    deploy_workflow.logger.info('Launching workflow defined by files in \'' + suite_path + '\'.',
                                False)
    deploy_workflow.logger.info('Experiment name: ' + experiment_name)

    # Launch the workflow
    # -------------------
    deploy_workflow.cylc_run_experiment()


# --------------------------------------------------------------------------------------------------
