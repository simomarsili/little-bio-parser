RECORDS = "[(0, 'VP54_CPSVP/90-227', '........LGTLKSITDKLRKLGGESSQPFIQFYKVQCMYIPLFSRVDGDNG......EITVSLIDDGKEAAGQDPIIQSITFDASQMAMVELSMNFFVEKKDMDFIGIHVSAENVPVQDRAYGSINLAFFTNEQSVPMMQEEKKSSYLMID..'), (1, 'Q6E6Y4_9VIRU/93-231', 'ttkvkitt-------MDKVTSLIKFEKFPFYRVDRLKILYIPLFSGENSEGK......NITFSIQDRSMVVAGKPKKISSATAPINKMSMIELSATYFVQSKDLSKIEFGYKAKGIPVSGRSFAAVYLAFYIHGDHFPATMRPKDPIVLLID..'), (2, 'A0A075IE34_9VIRU/105-247', '.iatmgrv-------VNLFKKATG-NEMPFVKFEKVQVMYIPLFQKTNEEDDpdkkipSMTVALVDKGQEEAGGDGIIQSITFRADEMALMELSMNFFVTRKDIEKIVVDACVDEIPVEGRAYGAMTIAFFVHEDYVPLRTELKPSTLMY--it')]"


def tests_dir():
    """Return None is no tests dir."""
    import os
    cwd = os.getcwd()
    basename = os.path.basename(cwd)
    if basename == 'tests':
        return cwd
    else:
        tests_dir = os.path.join(cwd, 'tests')
        if os.path.exists(tests_dir):
            return tests_dir


def test_0():
    assert 1 == 1


def test_fasta():
    import os
    import lilbio
    fname = os.path.join(tests_dir(), '1.fa')
    a = [record for record in lilbio.parse(fname, 'fasta')]
    assert repr(a) == RECORDS


def test_stockholm():
    import os
    import lilbio
    fname = os.path.join(tests_dir(), '1.sto')
    a = [record for record in lilbio.parse(fname, 'stockholm')]
    assert repr(a) == RECORDS
