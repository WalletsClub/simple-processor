# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_instruction_identification, make_biz_message_identification, make_e2e_identification


def template():
    """ pacs.028 message template """
    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
            "CreDt": "${AppHdr_CreDt}",
            "Fr": {
                "FIId": {
                    "FinInstnId": {
                        "ClrSysMmbId": {
                            "MmbId": "${AppHdr_Fr_MmbId}"
                        }
                    }
                }
            },
            "MsgDefIdr": "pacs.028.001.09",
            "To": {
                "FIId": {
                    "FinInstnId": {
                        "ClrSysMmbId": {
                            "MmbId": "${AppHdr_To_MmbId}"
                        }
                    }
                }
            }
        },
        "Document": {
            "FIToFIPmtStsReq": {
                "GrpHdr": {
                    "MsgId": "${GrpHdr_MsgId}",
                    "CreDtTm": "${GrpHdr_CreDtTm}"
                },
                "TxInf": {
                    "OrgnlGrpInf": {
                        "OrgnlMsgId": "${OrgnlGrpInf_OrgnlMsgId}",
                        "OrgnlMsgNmId": "${OrgnlGrpInf_OrgnlMsgNmId}",
                        "OrgnlCreDtTm": "${OrgnlGrpInf_OrgnlCreDtTm}"
                    },
                    "InstgAgt": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${InstgAgt_MmbId}"
                            }
                        }
                    },
                    "InstdAgt": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${InstdAgt_MmbId}"
                            }
                        }
                    }
                }
            }
        }
    }

    return json.dumps(tpl)


def build(**kwargs):
    """ build message, return dict """
    t = Template(template())
    content = t.substitute(**kwargs)

    return json.loads(content)


def bake(my_pid, net_pid, cp_pid):
    """ Bake a pacs.028 message """

    hdr_biz_msg_id = make_biz_message_identification(my_pid)
    doc_msg_id = make_instruction_identification(my_pid)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_pid,
        'AppHdr_To_MmbId': net_pid,
        'GrpHdr_MsgId': doc_msg_id,
        'GrpHdr_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'OrgnlGrpInf_OrgnlMsgId': '',
        'OrgnlGrpInf_OrgnlMsgNmId': '',
        'OrgnlGrpInf_OrgnlCreDtTm': '',
        'InstgAgt_MmbId': my_pid,
        'InstdAgt_MmbId': cp_pid,
    }

    message = build(**kwargs)

    return message
