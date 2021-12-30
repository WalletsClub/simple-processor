# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_biz_message_identification, make_instruction_identification


def template():
    """ camt.056 message template """
    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
            "MsgDefIdr": "camt.056.001.09",
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
            "FIToFIPmtCxlReq": {
                "Assgnmt": {
                    "Id": "${Document_Assgnmt_Id}",
                    "Assgnr": {
                        "Agt": {
                            "FinInstnId": {
                                "ClrSysMmbId": {
                                    "MmbId": '${Document_Assgnr_MmbId}'
                                }
                            }
                        }
                    },
                    "Assgne": {
                        "Agt": {
                            "FinInstnId": {
                                "ClrSysMmbId": {
                                    "MmbId": '${Document_Assgne_MmbId}'
                                }
                            }
                        }
                    },
                    "CreDtTm": "${Document_CreDtTm}"
                },
                "Case": {
                    "Id": "${Document_Case_Id}",
                    "Cretr": {
                        "Agt": {
                            "FinInstnId": {
                                "ClrSysMmbId": {
                                    "MmbId": "${Document_Cretr_MmbId}"
                                }
                            }
                        }
                    }
                },
                "Undrlyg": {
                    "OrgnlGrpInfAndCxl": {
                        "OrgnlMsgId": "${Document_OrgnlMsgId}",
                        "OrgnlMsgNmId": "${Document_OrgnlMsgNmId}",
                    },
                    "TxInf": {
                        "OrgnlInstrId": "${Document_OrgnlInstrId}",
                        "OrgnlEndToEndId": "${Document_OrgnlEndToEndId}",
                        "OrgnlTxId": "${Document_OrgnlTxId}",
                        "OrgnlClrSysRef": "NOT-PROVIDE",
                        "OrgnlIntrBkSttlmAmt": {
                            "Amount": "${Document_Tx_Orgn_Amount}",
                            "Ccy": "${Document_Tx_Orgn_Ccy}",
                        },
                        "OrgnlIntrBkSttlmDt": "${Document_OrgnlIntrBkSttlmDt}",
                        "CxlRsnInf": {
                            "Rsn": {
                                "Cd": "${Document_CxlRsn_Cd}"
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
    """ Bake a camt.056 message """

    hdr_biz_msg_id = make_biz_message_identification(my_pid)

    doc_case_id = make_instruction_identification(my_pid)
    doc_ass_id = make_instruction_identification(my_pid)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_pid,
        'AppHdr_To_MmbId': net_pid,
        'Document_Assgnmt_Id': doc_ass_id,
        'Document_Assgnr_MmbId': my_pid,
        'Document_Assgne_MmbId': cp_pid,
        'Document_CreDtTm': str(datetime.now().astimezone(None).isoformat()),  # ISO8601
        'Document_Case_Id': doc_case_id,
        'Document_Cretr_MmbId': my_pid,
        'Document_OrgnlMsgId': '',
        'Document_OrgnlMsgNmId': '',
        'Document_OrgnlInstrId': '',
        'Document_OrgnlEndToEndId': '',
        'Document_OrgnlTxId': '',
        'Document_Tx_Orgn_Amount': '',
        'Document_Tx_Orgn_Ccy': '',
        'Document_OrgnlIntrBkSttlmDt': '',
        'Document_CxlRsn_Cd': 'CUST'  # refer: RTP - Usage in camt.056
    }

    message = build(**kwargs)

    return message
