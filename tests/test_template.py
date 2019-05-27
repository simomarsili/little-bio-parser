# -*- coding: utf-8 -*-
# pylint:disable=missing-docstring
import os

import lilbio

RECORDS = "[('VP54_CPSVP/90-227', '........LGTLKSITDKLRKLGGESSQPFIQFYKVQCMYIPLFSRVDGDNG......EITVSLIDDGKEAAGQDPIIQSITFDASQMAMVELSMNFFVEKKDMDFIGIHVSAENVPVQDRAYGSINLAFFTNEQSVPMMQEEKKSSYLMID..'), ('Q6E6Y4_9VIRU/93-231', 'ttkvkitt-------MDKVTSLIKFEKFPFYRVDRLKILYIPLFSGENSEGK......NITFSIQDRSMVVAGKPKKISSATAPINKMSMIELSATYFVQSKDLSKIEFGYKAKGIPVSGRSFAAVYLAFYIHGDHFPATMRPKDPIVLLID..'), ('A0A075IE34_9VIRU/105-247', '.iatmgrv-------VNLFKKATG-NEMPFVKFEKVQVMYIPLFQKTNEEDDpdkkipSMTVALVDKGQEEAGGDGIIQSITFRADEMALMELSMNFFVTRKDIEKIVVDACVDEIPVEGRAYGAMTIAFFVHEDYVPLRTELKPSTLMY--it')]"  # pylint:disable=line-too-long


def tests_dir():
    """Return None is no tests dir."""
    cwd = os.getcwd()
    basename = os.path.basename(cwd)
    tdir = None
    if basename == 'tests':
        tdir = cwd
    else:
        tdir = os.path.join(cwd, 'tests')
        if not os.path.exists(tdir):
            tdir = None
    return tdir


def test_fasta():
    fname = os.path.join(tests_dir(), '1.fa')
    a = list(lilbio.parse(fname, 'fasta'))
    assert repr(a) == RECORDS


def test_stockholm():
    fname = os.path.join(tests_dir(), '1.sto')
    a = list(lilbio.parse(fname, 'stockholm'))
    assert repr(a) == RECORDS
