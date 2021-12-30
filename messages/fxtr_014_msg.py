# -*- coding:utf-8 -*-

import json
import random
from datetime import datetime
from string import Template

from money import Money
from identifier import make_biz_message_identification, make_agreement_identification


def template():
    """ 消息模板, 返回一个字符串 """
    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
            "MsgDefIdr": "fxtr.014.001.04",
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
            "FXTradInstr": {
                "TradInf": {
                    "TradDt": "${Document_TradDt}",
                    "OrgtrRef": "${Document_OrgtrRef}"
                },
                "TradgSdId": {
                    "SubmitgPty": {
                        "NmAndAdr": {
                            "Name": "${Document_TSMM}",
                            "AltrntvIdr": "${Document_TSMA}"
                        }
                    },
                    "TradPty": {
                        "NmAndAdr": {
                            "Name": "${Document_TTMM}",
                            "AltrntvIdr": "${Document_TTMA}"
                        }
                    }
                },
                "CtrPtySdId": {
                    "SubmitgPty": {
                        "NmAndAdr": {
                            "Name": "${Document_CSMM}",
                            "AltrntvIdr": "${Document_CSMA}"
                        }
                    },
                    "TradPty": {
                        "NmAndAdr": {
                            "Name": "${Document_CTMM}",
                            "AltrntvIdr": "${Document_CTMA}"
                        }
                    }
                },
                "TradAmts": {
                    "TradgSdSellAmt": "${Document_TradgSdSellAmt}",
                    "TradgSdSellCcy": "${Document_TradgSdSellCcy}",
                    "TradgSdBuyAmt": "${Document_TradgSdBuyAmt}",
                    "TradgSdBuyCcy": "${Document_TradgSdBuyCcy}",
                    "SttlmDt": "${Document_SttlmDt}"
                },
                "AgrdRate": {
                    "XchgRate": "${Document_XchgRate}"
                },
                "TradgSdSttlmInstrs": {
                    "DlvryAgt": {
                        "NmAndAdr": {
                            "Name": "${Document_DMM}",
                            "AltrntvIdr": "${Document_DMA}"
                        }
                    },
                    "RcvgAgt": {
                        "NmAndAdr": {
                            "Name": "${Document_RMM}",
                            "AltrntvIdr": "${Document_RMA}"
                        }
                    }
                }
            }
        }
    }

    return json.dumps(tpl)


def build(**kwargs):
    """ 通过模板构建消息体, 返回一个dict """
    t = Template(template())
    content = t.substitute(**kwargs)

    return json.loads(content)


def bake(my_pid, net_pid, cp_pid, sell_ccy='HKD', buy_ccy='USD'):
    """ 生成一个完整的&正确的默认消息 """
    hdr_biz_msg_id = make_biz_message_identification(my_pid)
    # 这相当于一个双方协商好的FX交易订单号，NET会以此为依据来匹配双边的FX交易
    ref_id = make_agreement_identification(my_pid)

    # 这里只支持USD和HKD的就行了，不需要支持其他币种，汇率就定在 1 USD = 7.77 HKD

    fx_rate = random.choice([7.7777, 7.7681, 7.7759, 7.7682, 7.7849, 7.7650])
    usd_amt = random.randint(100, 1000)

    if sell_ccy == 'USD' and buy_ccy == 'HKD':
        sell_m = Money(usd_amt, 'USD')
        buy_m = Money(round(usd_amt * fx_rate, 2), 'HKD')
    else:
        buy_m = Money(usd_amt, 'USD')
        sell_m = Money(round(usd_amt * fx_rate, 2), 'HKD')

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_pid,
        'AppHdr_To_MmbId': net_pid,
        'Document_TradDt': str(datetime.now().strftime('%Y-%m-%d')),
        'Document_OrgtrRef': ref_id,
        'Document_TSMM': my_pid[:4],
        'Document_TSMA': my_pid,
        'Document_TTMM': my_pid[:4],
        'Document_TTMA': my_pid,
        'Document_CSMM': 'XXX',
        'Document_CSMA': cp_pid,
        'Document_CTMM': 'XXX',
        'Document_CTMA': cp_pid,
        'Document_TradgSdSellAmt': str(sell_m.amount),
        'Document_TradgSdSellCcy': str(sell_m.currency),
        'Document_TradgSdBuyAmt': str(buy_m.amount),
        'Document_TradgSdBuyCcy': str(buy_m.currency),
        'Document_SttlmDt': str(datetime.now().strftime('%Y-%m-%d')),
        'Document_XchgRate': round(buy_m.amount / sell_m.amount, 4),
        'Document_DMM': 'ABank',
        'Document_DMA': 'ABNKHKHHXXX',
        'Document_RMM': 'ABank',
        'Document_RMA': 'ABNKHKHHXXX'
    }

    # 买卖反过来
    if fr == 'z':
        kwargs['Document_TradgSdSellAmt'] = str(buy_m.amount)
        kwargs['Document_TradgSdSellCcy'] = str(buy_m.currency)
        kwargs['Document_TradgSdBuyAmt'] = str(sell_m.amount)
        kwargs['Document_TradgSdBuyCcy'] = str(sell_m.currency)
        kwargs['Document_XchgRate'] = round(sell_m.amount / buy_m.amount, 4)

    message = build(**kwargs)

    # print(message)

    return message


def bake_fxtr_014_from_fxtr_017(fxtr_017_message):
    """ 根据017生成014 """
    from xpay.config import my_participant_id as x_participant_id
    from zremit.config import my_participant_id as z_participant_id

    tradg_sd_id = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradgSdId']['SubmitgPty']['NmAndAdr'][
        'AltrntvIdr']

    ctrpty_sd_id = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['CtrPtySdId']['SubmitgPty']['NmAndAdr'][
        'AltrntvIdr']

    # if ctrpty_sd_id == x_participant_id:
    #     from xpay.config import my_participant_id, cp_participant_id
    # elif ctrpty_sd_id == z_participant_id:
    #     from zremit.config import my_participant_id, cp_participant_id
    # else:
    #     from xpay.config import my_participant_id, cp_participant_id

    hdr_biz_msg_id = make_biz_message_identification(my_participant_id)

    # 获取原消息里面的ref，这两个是作为唯一匹配交易的要素
    ref_id = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradInf']['OrgtrRef']

    i_sell_amt = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradAmts']['TradgSdBuyAmt']
    i_sell_ccy = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradAmts']['TradgSdBuyCcy']

    i_buy_amt = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradAmts']['TradgSdSellAmt']
    i_buy_ccy = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradAmts']['TradgSdSellCcy']

    sttlm_dt = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradAmts']['SttlmDt']

    tradg_sd_name = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['TradgSdId']['SubmitgPty']['NmAndAdr'][
        'Name']

    ctrpty_sd_name = fxtr_017_message['Document']['FXTradStsAndDtlsNtfctn']['CtrPtySdId']['SubmitgPty']['NmAndAdr'][
        'Name']

    sell_money = Money(i_sell_amt, i_sell_ccy)
    buy_money = Money(i_buy_amt, i_buy_ccy)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_participant_id,
        'AppHdr_To_MmbId': wnet_id,
        'Document_TradDt': str(datetime.now().strftime('%Y-%m-%d')),
        'Document_OrgtrRef': ref_id,
        'Document_TSMM': ctrpty_sd_name,
        'Document_TSMA': my_participant_id,
        'Document_TTMM': ctrpty_sd_name,
        'Document_TTMA': my_participant_id,
        'Document_CSMM': tradg_sd_name,
        'Document_CSMA': tradg_sd_id,
        'Document_CTMM': tradg_sd_name,
        'Document_CTMA': tradg_sd_id,
        'Document_TradgSdSellAmt': str(sell_money.amount),
        'Document_TradgSdSellCcy': str(sell_money.currency),
        'Document_TradgSdBuyAmt': str(buy_money.amount),
        'Document_TradgSdBuyCcy': str(buy_money.currency),
        'Document_SttlmDt': sttlm_dt,
        # ISO标准里面的汇率 = Base currency / Quote currency
        # X/Y = aaa/bbb
        # X: Base currency，这玩意是“货”，也就是你“买”的货币
        # Y: Quote currency / term currency / offer currency，这玩意是“钱”，也就是你愿意付出的钱（本质上就是你卖出的货币）
        'Document_XchgRate': round(buy_money.amount / sell_money.amount, 4),
        'Document_DMM': 'ABank',
        'Document_DMA': 'ABNKHKHHXXX',
        'Document_RMM': 'ABank',
        'Document_RMA': 'ABNKHKHHXXX'
    }

    message = build(**kwargs)

    # print(message)

    return message
