import pandas as pd

from .spocfile import SpocFile
from .ctypes import (
    Column, HLColumn, SLColumn, WSColumn, TagParam, FileParam,
    XColumn, YColumn)


class HL(SpocFile):
    object_id = Column('OBJECTID')
    id = pid = HLColumn('CODE')
    naam = Column('NAAM')
    types = Column('TYPES')
    shortname = Column('SHORTNAME')
    icon = Column('ICON')
    tooltop = Column('TOOLTIP')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    namespace = Column('NAMESPACE')
    x = XColumn('X')
    y = YColumn('Y')
    commentaar = Column('COMMENTAAR')
    area = Column('DS_GBD')

    def __init__(self):
        super().__init__()

        self.sl = SL()
        self.ws = WS()

    def __iter__(self):
        return iter((self, self.sl, self.ws))

    def sublocations(self, id: str) -> dict[str, pd.Index]:
        return {str(i).lower(): i.ids_by_pids(id) for i in self}

    def get_param_matches(self, id):
        sublocations = self.sublocations(id)
        _ = sublocations.pop(str(self))

        matches = []
        for spocfile in sublocations:
            for id in sublocations[spocfile]:
                matches += getattr(self, spocfile).get_param_matches(id)
        return matches


class SL(SpocFile):
    objectid = Column('OBJECTID')
    id = SLColumn('CODE')
    name = Column('NAAM')
    type = Column('TYPE')
    area = Column('GEBIED')
    shortname = Column('SHORTNAME')
    icon = Column('ICON')
    tooltip = Column('TOOLTIP')
    fotoid = Column('Foto_id')
    pid = HLColumn('PARENTLOCATIONID', unique=False)
    hbov = Column('HBOV')
    hben = Column('HBEN')
    hbovps = Column('HBOV_PS')
    hbenps = Column('HBEN_PS')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    namespace = Column('NAMESPACE')
    x = XColumn('X')
    y = YColumn('Y')
    commentaar = Column('COMMENTAAR')

    def __init__(self):
        super().__init__()

        self.sl_tags = SL_TAGS()
        self.sl_ti_h2go_tags = SL_TI_H2GO_TAGS()
        self.damo_pomp = DAMO_pomp()
        self.damo_stuw = DAMO_stuw()

    def __iter__(self):
        return iter((self.sl_tags, self.sl_ti_h2go_tags, self.damo_pomp,
                     self.damo_stuw))

    def get_param_matches(self, id):
        return super().get_param_matches(self.sl_ti_h2go_tags, id)


class WS(SpocFile):
    id = WSColumn('ï»¿CODE')
    naam = Column('NAAM')
    type = Column('TYPE')
    shortname = Column('SHORTNAME')
    area = Column('GEBIED')
    icon = Column('ICON')
    tooltip = Column('TOOLTIP')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    namespace = Column('NAMESPACE')
    x = XColumn('X')
    y = YColumn('Y')
    pid = HLColumn('PARENTLOCATIONID', unique=False, empty=True, pattern=False)
    commentaar = Column('COMMENTAAR')
    scx_lcode = Column('SCX_Lcode')

    def __init__(self):
        super().__init__()

        self.ws_tags = WS_TAGS()
        self.ws_ti_h2go_tags = WS_TI_H2GO_TAGS()
        self.ws_validatie = WS_VALIDATIE()

    def __iter__(self):
        return iter((self.ws_tags, self.ws_ti_h2go_tags, self.ws_validatie))

    def get_param_matches(self, id):
        return super().get_param_matches(self.ws_ti_h2go_tags, id)


class SL_TAGS(SpocFile):
    shortname = Column('SHORTNAME')
    id = SLColumn('CODE')
    locationid = Column('LOCATIONID')
    source = Column('SOURCE')

    param_bs = TagParam('TAG_CGOO_BS', param='BS')
    param_tt = TagParam('TAG_CGOO_TT', param='TT')
    param_sh = TagParam('TAG_CGOO_SH', param='SH')
    param_sd = TagParam('TAG_CGOO_SD', param='SD')
    param_mwar = TagParam('TAG_CGOO_MWAR', param='MWAR')
    param_qb = TagParam('TAG_CGOO_Q_berekening', param='QB')
    param_od = TagParam('TAG_CGOO_OPEN_DICHT', param='OD')
    param_gkz = TagParam('TAG_CGOO_GKZ', param='GKZ')
    param_pf = TagParam('TAG_CGOO_FREQ', param='PF')
    param_a = TagParam('TAG_CGOO_A', param='A')
    param_so = TagParam('TAG_CGOO_SO', param='SO')

    tag_cgoo_q_meting = Column('TAG_CGOO_Q_meting')
    tag_cgoo_niveau_put = Column('TAG_CGOO_NIVEAU_PUT')
    tag_cgoo_qin = Column('TAG_CGOO_QIN')

    gecontroleerd = Column('GECONTROLEERD')
    tag_cgoo_bs_unit = Column('TAG_CGOO_BS_UNIT')
    tag_cgoo_q_berekening_unit = Column('TAG_CGOO_Q_berekening_UNIT')

    def __init__(self):
        super().__init__()

    def get_param_value(self, id, param):
        return super().field(id, param)


class SL_TI_H2GO_TAGS(SpocFile):
    id = SLColumn('SL_CODE')
    type = Column('TYPE')
    shortname = Column('SHORTNAME')
    ti_code = Column('TI_CODE')
    h2go_locid = Column('H2GO_LOCID')

    param_bs = FileParam('BS_0', param='BS', relation=SL_TAGS.param_bs)
    param_tt = FileParam('TT_0', param='TT', relation=SL_TAGS.param_tt)
    param_sh = FileParam('SH_0', param='SH', relation=SL_TAGS.param_sh)
    param_sd = FileParam('SD_0', param='SD', relation=SL_TAGS.param_sd)
    param_mwar = FileParam('MWAR_0', param='MWAR', relation=SL_TAGS.param_mwar)
    param_qb = FileParam('Q_B_0', param='QB', relation=SL_TAGS.param_qb)
    param_od = FileParam('OD_0', param='OD', relation=SL_TAGS.param_od)
    param_gkz = FileParam('GKZ_0', param='GKZ', relation=SL_TAGS.param_gkz)
    param_pf = FileParam('PF_0', param='PF', relation=SL_TAGS.param_pf)
    param_a = FileParam('A_0', param='A', relation=SL_TAGS.param_a)
    param_so = FileParam('SO_0', param='SO', relation=SL_TAGS.param_so)
    handh = FileParam('HANDH_0', param='HANDH')

    commentaar = Column('_COMMENTAAR')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        super().__init__()

    def get_param_value(self, id, param):
        return super().field(id, self.h2go_locid).concat(
            super().field(id, param))


class DAMO_pomp(SpocFile):
    versie1_alb = Column('Versie1_ALB')
    global_pomp_id = Column('GlobalpompID')
    objectid = Column('OBJECTID')
    id = SLColumn('CODE', unique=False)
    naam = Column('NAAM')
    typepomp = Column('TYPEPOMP')
    typeformule = Column('TYPEFORMULE')
    pompcap = Column('POMPCAP')
    max_ampere = Column('MAX_AMPERE')
    max_toer = Column('MAX_TOER')
    min_toer = Column('MIN_TOER')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        super().__init__()


class DAMO_stuw(SpocFile):
    objectid = Column('OBJECTID')
    id = SLColumn('CODE', unique=False)
    naam = Column('NAAM')
    type = Column('TYPE')
    typedebiet = Column('TYPEDEBIET')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    doorstroombreedte = Column('doorstroombreedte')
    drempelhoogte = Column('drempelhoogte')
    bovenkant_onderdoorlaat = Column('bovenkant_onderdoorlaat')
    kleplengte = Column('kleplengte')
    maximale_kruinhoogte = Column('maximale_kruinhoogte')
    c_onderdoorlaat = Column('c_onderdoorlaat')
    bodemhoogte_voor_overlaat = Column('Bodemhoogte_voor_overlaat')
    vorm_schuif = Column('vorm_schuif')
    type_schuifberekening = Column('Type_schuifberekening')
    factor_weff_macht0 = Column('Factor_weff_macht0')
    factor_weff_macht1 = Column('Factor_weff_macht1')
    factor_weff_macht2 = Column('Factor_weff_macht2')
    factor_well_macht3 = Column('Factor_weff_macht3')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        pass


class WS_TAGS(SpocFile):
    id = WSColumn('LOCATIONID')
    source = Column('SOURCE')

    param_hm = TagParam('TAG_CGOO_MNAP', param='HM')
    param_qm = TagParam('TAG_CGOO_Q', param='QM')

    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        super().__init__()

    def get_param_value(self, id, param):
        return super().field(id, param)


class WS_TI_H2GO_TAGS(SpocFile):
    naam = Column('NAAM')
    id = WSColumn('OW_CODE')
    fewsparam = Column('FEWS_PARAM')
    ti_code = Column('TI_CODE')
    h2go_locid = Column('H2GO_LOCID')

    param_hm = FileParam('H2GO_MEETPUNTID', param='HM',
                         relation=WS_TAGS.param_hm)
    param_qm = FileParam('H2GO_Q', param='QM', relation=WS_TAGS.param_qm)
    param_hmhand = FileParam('H2GO_HANDMEETPUNTID', param='HMHAND')

    comment = Column('COMMENT')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        super().__init__()

    def get_param_value(self, id, param):
        return super().field(id, self.h2go_locid).concat(
            super().field(id, param))


class WS_VALIDATIE(SpocFile):
    kw_naam = Column('KW Naam')
    hben_hbov = Column('Hben/Hbov')
    lcode = Column('Lcode')
    id = WSColumn('LOCID', unique=False)
    area = Column('gebied')
    startdate = Column('STARTDATE')
    enddate = Column('ENDDATE')
    win_smax = Column('WIN_SMAX')
    win_smin = Column('WIN_SMIN')
    ov_max = Column('OV_SMAX')
    ov_smin = Column('OV_SMIN')
    zom_smax = Column('ZOM_SMAX')
    zom_smin = Column('ZOM_SMIN')
    hardmax = Column('HARDMAX')
    hardmin = Column('HARDMIN')
    ratechange = Column('RATECHANGE')
    sr_dev = Column('SR_DEV')
    sr_period = Column('SR_PERIOD')
    sr0_5_dev = Column('SR0.5_DEV')
    sr0_5_period = Column('SR0.5_PERIOD')
    sr7_dev = Column('SR7_DEV')
    sr7_period = Column('SR7_PERIOD')
    ts_rate = Column('TS_RATE')
    ts_period = Column('TS_PERIOD')
    code = Column('code')
    opmerking = Column('opmerking')
    opemerking_zachte_grenzen = Column('opmerking zachte grenzen')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        super().__init__()
