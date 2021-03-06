# -*- coding:utf-8 -*-

import json
import random
from datetime import datetime
from string import Template
import logging

try:
    logging.getLogger('faker').setLevel(logging.FATAL)
    from faker import Faker
except Exception as e:
    pass

from identifier import make_instruction_identification, make_biz_message_identification, make_e2e_identification
from money import Money


def template():
    """ pain.013 message template """
    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
            "CreDt": "${AppHdr_CreDt}",
            "MsgDefIdr": "pain.013.001.09",
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
            "CdtrPmtActvtnReq": {
                "GrpHdr": {
                    "MsgId": "${Doc_GrpHdr_MsgId}",
                    "CreDtTm": "${Doc_GrpHdr_CreDtTm}",
                    "NbOfTxs": "1",
                    "CtrlSum": "${Doc_GrpHdr_CtrlSum}",
                    "InitgPty": {
                        "Id": {
                            "OrgId": {
                                "Othr": {
                                    "Id": "${Doc_GrpHdr_InitgPty_Id}"
                                }
                            }
                        }
                    }
                },
                "PmtInf": [
                    {
                        "PmtInfId": "${Doc_PmtInf_PmtInfId}",
                        "PmtTpInf": {
                            "CtgyPurp": {
                                "Cd": "${CtgyPurp_Cd}"
                            }
                        },
                        "PmtMtd": "TRF",
                        "ReqdExctnDt": "${Doc_PmtInf_ReqdExctnDt}",
                        "Dbtr": {
                            "Nm": "${Doc_Dbtr_Nm}"
                        },
                        "DbtrAcct": {
                            "Id": {
                                "OrgId": {
                                    "Othr": {
                                        "Id": "${Doc_DbtrAcct_Id}"
                                    }
                                }
                            }
                        },
                        "DbtrAgt": {
                            "FinInstnId": {
                                "ClrSysMmbId": {
                                    "MmbId": "${Doc_DbtrAgt_Id}"
                                }
                            }
                        },
                        "CdtTrfTx": [
                            {
                                "PmtId": {
                                    "InstrId": "${Doc_InstrId}",
                                    "EndToEndId": "${Doc_EndToEndId}"
                                },
                                "PmtTpInf": {
                                    "SvcLvl": {
                                        "Cd": "SDVA"
                                    },
                                    "LclInstrm": {
                                        "Prtry": "BUSINESS"
                                    }
                                },
                                "Amt": {
                                    "InstdAmt": "${Doc_InstdAmt}",
                                    "Ccy": "${Doc_Ccy}"
                                },
                                "ChrgBr": "SLEV",
                                "CdtrAgt": {
                                    "FinInstnId": {
                                        "ClrSysMmbId": {
                                            "MmbId": "${Doc_CdtrAgt_Id}"
                                        }
                                    }
                                },
                                "Cdtr": {
                                    "Nm": "${Doc_Cdtr_Nm}"
                                },
                                "CdtrAcct": {
                                    "Id": {
                                        "OrgId": {
                                            "Othr": {
                                                "Id": "${Doc_CdtrAcct_Id}"
                                            }
                                        }
                                    }
                                },
                                "RmtInf": {
                                    "Ustrd": "This is a message from creditor"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }

    return json.dumps(tpl)


def build(**kwargs):
    """ build message, return dict """
    t = Template(template())
    content = t.substitute(**kwargs)

    return json.loads(content)


def bake(creditor_pid, net_pid, debtor_pid, ccy='USD', amt=None):
    """ Bake a pain.013 message """

    hdr_biz_msg_id = make_biz_message_identification(debtor_pid)
    doc_msg_id = make_instruction_identification(debtor_pid)
    doc_e2e_msg_id = make_e2e_identification(debtor_pid)

    if amt is None:
        # random 1 ~ 10 amount
        money = Money(round(random.uniform(1, 10), 2), ccy)
    else:
        money = Money(abs(amt), ccy)

    fake = Faker()

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': creditor_pid,
        'AppHdr_To_MmbId': net_pid,
        'Doc_GrpHdr_MsgId': doc_msg_id,
        'Doc_GrpHdr_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'Doc_GrpHdr_CtrlSum': str(money.amount),
        'Doc_GrpHdr_InitgPty_Id': creditor_pid,
        'CtgyPurp_Cd': 'RQTP',
        'Doc_PmtInf_PmtInfId': doc_e2e_msg_id,
        'Doc_PmtInf_ReqdExctnDt': str(datetime.now().strftime('%Y-%m-%d')),
        'Doc_Dbtr_Nm': fake.name(),
        'Doc_DbtrAcct_Id': fake.md5(),
        'Doc_DbtrAgt_Id': debtor_pid,
        'Doc_InstrId': doc_e2e_msg_id,
        'Doc_EndToEndId': doc_e2e_msg_id,
        'Doc_InstdAmt': str(money.amount),
        'Doc_Ccy': money.currency.code,
        'Doc_CdtrAgt_Id': creditor_pid,
        'Doc_Cdtr_Nm': fake.name(),
        'Doc_CdtrAcct_Id': fake.md5()
    }

    message = build(**kwargs)

    return message


def bake_rtp(creditor_pid, net_pid, debtor_pid, ccy='USD', amt=None):
    """ bake RtP Message """
    message = bake(creditor_pid, net_pid, debtor_pid, ccy, amt)
    message['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['PmtTpInf']['CtgyPurp']['Cd'] = 'RQTP'

    return message


def bake_rff(creditor_pid, net_pid, debtor_pid, ccy='USD', amt=None):
    """ bake RfF Message """
    message = bake(creditor_pid, net_pid, debtor_pid, ccy, amt)
    message['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['PmtTpInf']['CtgyPurp']['Cd'] = 'RQFF'
    message['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['Dbtr']['Nm'] = debtor_pid[:4]
    message['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['CdtTrfTx'][0]['Cdtr']['Nm'] = creditor_pid[:4]
    message['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['CdtTrfTx'][0]['RmtInf']['Ustrd'] = 'Request for fee'

    return message
