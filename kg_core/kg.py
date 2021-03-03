#   Copyright (c) 2018, EPFL/Human Brain Project PCO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from copy import deepcopy

from kg_core.auth import TokenHandler, RequestsWithTokenHandler
from kg_core.models import KGResult, Stage, Pagination, ResponseConfiguration


class KGv3(RequestsWithTokenHandler):
    KG_VERSION = "v3-beta"

    def __init__(self, host: str, token_handler: TokenHandler):
        super(KGv3, self).__init__(f"https://{host}/{KGv3.KG_VERSION}", token_handler)

    def next_page(self, result: KGResult):
        remaining_items = result.total() - (result.start_from() + result.size())
        if remaining_items > 0:
            if result.request_args:
                new_args = deepcopy(result.request_args)
                if "params" not in new_args:
                    new_args["params"] = {}
                new_args["params"]["from"] = result.start_from() + result.size()
                return self._do_request(new_args, result.request_payload)
        return None

    def queries(self, query: dict, stage: Stage):
        return self.post("/queries", query, {"stage": stage})

    def instances(self, stage: Stage, target_type: str, space: str = None, search_by_label: str = None, response_configuration: ResponseConfiguration = ResponseConfiguration(),
                  pagination: Pagination = Pagination()) -> KGResult:
        return self.get("/instances",
                        {
                            "stage": stage,
                            "type": target_type,
                            "space": space,
                            "searchByLabel": search_by_label,
                            "returnPayload": response_configuration.return_payload,
                            "returnPermissions": response_configuration.return_permissions,
                            "returnAlternatives": response_configuration.return_alternatives,
                            "returnEmbedded": response_configuration.return_embedded,
                            "returnIncomingLinks": response_configuration.return_incoming_links,
                            "sortByLabel": response_configuration.sort_by_label,
                            "from": pagination.start_from,
                            "size": pagination.size
                        })
