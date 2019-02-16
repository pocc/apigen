# -*- coding: utf-8 -*-
"""
oag_meraki --lang <lang>...

OPTIONS:
  -l, --lang <lang>     Output language. Can be specified multiple times.

SEE ALSO:
  OpenAPI Generator: https://github.com/OpenAPITools/openapi-generator
"""
import docopt


def get_cli_args():
    """CLI entry point"""
    return docopt.docopt(__doc__)
