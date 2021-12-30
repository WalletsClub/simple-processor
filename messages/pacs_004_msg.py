# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_biz_message_identification, make_instruction_identification


def template():
    """ pacs.004 message template """

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
            "MsgDefIdr": "pacs.004.001.08",
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
            "PmtRtr": {
                "GrpHdr": {
                    "MsgId": "${GrpHdr_MsgId}",
                    "CreDtTm": "${GrpHdr_CreDtTm}",
                    "NbOfTxs": "1",
                    "SttlmInf": {
                        "SttlmMtd": "CLRG",
                        "ClrSys": {
                            "Cd": "WNET"
                        }
                    }
                },
                "TxInf": {
                    "RtrId": "${TxInf_RtrId}",
                    "OrgnlGrpInf": {
                        "OrgnlMsgId": "${OrgnlGrpInf_OrgnlMsgId}",
                        "OrgnlMsgNmId": "${OrgnlGrpInf_OrgnlMsgNmId}"
                    },
                    "OrgnlInstrId": "${TxInf_OrgnlInstrId}",
                    "OrgnlEndToEndId": "${TxInf_OrgnlEndToEndId}",
                    "OrgnlTxId": "${TxInf_OrgnlTxId}",
                    "RtrdIntrBkSttlmAmt": {
                        "Ccy": "${RtrdIntrBkSttlmAmt_Ccy}",
                        "Amount": "${RtrdIntrBkSttlmAmt_Amt}"
                    },
                    "IntrBkSttlmDt": "${TxInf_IntrBkSttlmDt}",
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
                    },
                    "RtrRsnInf": {
                        "Rsn": {
                            "Prtry": "FOCR"
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
    """ Bake a pacs.004 message """

    hdr_biz_msg_id = make_biz_message_identification(my_pid)
    doc_msg_id = make_instruction_identification(my_pid)
    refund_id = make_instruction_identification(my_pid)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_pid,
        'AppHdr_To_MmbId': net_pid,
        'GrpHdr_MsgId': doc_msg_id,
        'GrpHdr_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'TxInf_RtrId': refund_id,
        'OrgnlGrpInf_OrgnlMsgId': '',
        'OrgnlGrpInf_OrgnlMsgNmId': '',
        'TxInf_OrgnlInstrId': '',
        'TxInf_OrgnlEndToEndId': '',
        'TxInf_OrgnlTxId': '',
        'RtrdIntrBkSttlmAmt_Ccy': '',
        'RtrdIntrBkSttlmAmt_Amt': '',
        'TxInf_IntrBkSttlmDt': str(datetime.now().strftime('%Y-%m-%d')),
        'InstgAgt_MmbId': my_pid,
        'InstdAgt_MmbId': cp_pid
    }

    message = build(**kwargs)

    return message
