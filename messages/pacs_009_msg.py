# -*- coding:utf-8 -*-

import json
import random
from datetime import datetime
from string import Template
import logging

from identifier import make_instruction_identification, make_biz_message_identification, make_e2e_identification
from money import Money


def template():
    """ pacs.009 message template """
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
            "MsgDefIdr": "pacs.009.001.10",
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
            "FICdtTrf": {
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
                "CdtTrfTxInf": {
                    "PmtId": {
                        "InstrId": "${PmtId_InstrId}",
                        "EndToEndId": "${PmtId_EndToEndId}",
                        "TxId": "${PmtId_TxId}"
                    },
                    "PmtTpInf": {
                        "SvcLvl": {
                            "Cd": "SDVA"
                        },
                        "LclInstrm": {
                            "Prtry": "BUSINESS"
                        }
                    },
                    "IntrBkSttlmAmt": {
                        "Ccy": "${IntrBkSttlmAmt_Ccy}",
                        "Amount": "${IntrBkSttlmAmt_Amount}"
                    },
                    "IntrBkSttlmDt": "${IntrBkSttlmDt}",
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
                    "Dbtr": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${Dbtr_MmbId}"
                            }
                        }
                    },
                    "Cdtr": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${Cdtr_MmbId}"
                            }
                        }
                    },
                    "Purp": {
                        "Prtry": "FCOL"  # FCOL = FeeCollection
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


def bake(debtor_pid, net_pid, creditor_pid, ccy='USD', amt=None):
    """ Bake a pacs.009 message """

    hdr_biz_msg_id = make_biz_message_identification(debtor_pid)
    doc_msg_id = make_instruction_identification(debtor_pid)
    doc_e2e_msg_id = make_e2e_identification(debtor_pid)

    if amt is None:
        # random 1 ~ 10 amount
        money = Money(round(random.uniform(1, 10), 2), ccy)
    else:
        money = Money(abs(amt), ccy)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': debtor_pid,
        'AppHdr_To_MmbId': net_pid,
        'GrpHdr_MsgId': doc_msg_id,
        'IntrBkSttlmDt': str(datetime.now().strftime('%Y-%m-%d')),
        'GrpHdr_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'IntrBkSttlmAmt_Amount': str(money.amount),
        'IntrBkSttlmAmt_Ccy': money.currency.code,
        'PmtId_InstrId': doc_e2e_msg_id,
        'PmtId_EndToEndId': doc_e2e_msg_id,
        'PmtId_TxId': doc_e2e_msg_id,
        'InstgAgt_MmbId': debtor_pid,
        'Dbtr_MmbId': debtor_pid,
        'InstdAgt_MmbId': creditor_pid,
        'Cdtr_MmbId': creditor_pid
    }

    message = build(**kwargs)

    return message
