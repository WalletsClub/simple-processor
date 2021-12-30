# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_biz_message_identification, make_instruction_identification


def template():
    """ camt.016 message template """
    
    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
            "MsgDefIdr": "camt.016.001.04",
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
            "GetCcyXchgRate": {
                "MsgHdr": {
                    "MsgId": "${Document_MsgId}",
                    "CreDtTm": "${Document_CreDtTm}"
                },
                "CcyQryDef": {
                    "NewCrit": {
                        "SchCrit": {
                            "SrcCcy": "${Document_SrcCcy}",
                            "TrgtCcy": "${Document_TrgtCcy}"
                        }
                    }
                },
                "SplmtryData": {
                    "Envlp": {
                        "OrgtrRef": "${Document_OrgtrRef}",
                        "TradgSdId": {
                            "FIId": {
                                "FinInstnId": {
                                    "ClrSysMmbId": {
                                        "MmbId": "${Document_Td_MmbId}"
                                    }
                                }
                            }
                        },
                        "CtrPtySdId": {
                            "FIId": {
                                "FinInstnId": {
                                    "ClrSysMmbId": {
                                        "MmbId": "${Document_Cp_MmbId}"
                                    }
                                }
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


def bake(my_pid, net_pid, cp_pid, source_ccy='HKD', target_ccy='USD'):
    """ Bake a camt.016 message """

    hdr_biz_msg_id = make_biz_message_identification(my_pid)
    doc_msg_id = make_instruction_identification(my_pid)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_pid,
        'AppHdr_To_MmbId': net_pid,
        'Document_MsgId': doc_msg_id,
        'Document_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'Document_SrcCcy': source_ccy,
        'Document_TrgtCcy': target_ccy,
        'Document_OrgtrRef': hdr_biz_msg_id,
        'Document_Td_MmbId': my_pid,
        'Document_Cp_MmbId': cp_pid,
    }

    message = build(**kwargs)

    return message
