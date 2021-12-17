# -*- coding:utf-8 -*-

from util import deep_get, s, f


class Pacs002Processor(object):
    def __init__(self):
        pass

    def process_pacs_002_for_pace_008_from_net(self, pacs_002_message):
        """ Process pacs.002 message from WalletsNet:
            (1) if RCVD: Debit/Credit your user's account
            (2) if RJCT: Do nothing and alert reason to your user
        """

        e2e_id = pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['OrgnlInstrId']
        status = pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['TxSts']
        reason = deep_get(pacs_002_message, 'Document.FIToFIPmtStsRpt.TxInfAndSts.StsRsnInf.Rsn.Cd')

        if status == 'RCVD':
            print(s("Credit transfer succeeded, e2e transaction ID is: {0}".format(e2e_id)))
            print("Debit/Credit your user's account here...")
        elif status == 'RJCT':
            print(f("Credit transfer failed, e2e transaction ID is: {0}".format(e2e_id)))
            print("Alert the reason to your user, reason: {0}".format(reason))
        else:
            pass

    def process_pacs_002_for_camt_056_from_net(self, pacs_002_message):
        """ Process pacs.002 message from WalletsNet:
            (1) if RCVD: tell your user that the refund request has been forwarded to the creditor FI
                (1.1) if the creditor FI approves, you will receive positive camt.029 & pacs.008 messages later
                (1.2) if the creditor FI rejects, you will receive negative camt.029 message later
            (2) if RJCT: means the refund request has been rejected by WalletsNet due to some error set,
                you may do some investigation and retry again
        """

        status = pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['TxSts']
        reason = deep_get(pacs_002_message, 'Document.FIToFIPmtStsRpt.TxInfAndSts.StsRsnInf.Rsn.Cd')

        if status == 'RCVD':
            print(s("Your refund request has been forwarded to the creditor FI"))
            print("Notify your user some information here...")
        elif status == 'RJCT':
            print(f("Your refund request has been rejected by WalletsNet, the reason is: {0}".format(reason)))
        else:
            pass

    def process_pacs_002_from_net(self, pacs_002_message):
        """ pacs.002 categories:
            (1) feedback message for pacs.008;
            (2) feedback message for camt.056
        """
        try:
            ref_msg_scheme = pacs_002_message['Document']['FIToFIPmtStsRpt']['OrgnlGrpInfAndSts']['OrgnlMsgNmId'][:8]

            if ref_msg_scheme == 'pacs.008':
                self.process_pacs_002_for_pace_008_from_net(pacs_002_message)
            elif ref_msg_scheme == 'camt.056':
                self.process_pacs_002_for_camt_056_from_net(pacs_002_message)
            else:
                pass
        except:
            pass
