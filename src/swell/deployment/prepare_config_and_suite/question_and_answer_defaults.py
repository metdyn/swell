# (C) Copyright 2021- United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.


# --------------------------------------------------------------------------------------------------


from typing import Union
from datetime import datetime as dt


class GetAnswerDefaults:

    def get_answer(self, key: str, val: dict) -> Union[int, float, str, dt]:
        return val['default_value']

# --------------------------------------------------------------------------------------------------
