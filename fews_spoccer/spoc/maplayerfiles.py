import pandas as pd
import numpy as np

from .spocfile import SpocFile
from .ctypes import (
    Column, HLColumn, SLColumn, WSColumn, Param, TagParam, FileParam,
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
        self.sl = SL()
        self.ws = WS()

    def __iter__(self):
        return iter((self, self.sl, self.ws))

    def sublocations(self, id: str) -> dict[str, pd.Index]:
        return {str(i): i.ids_by_pids(id) for i in self}

    def param_value_matches(self, id: str, exclude_empty):
        '''
        Connect values that share the same parameter at HL level
        '''
        sublocations = self.sublocations(id)
        matches = {}

        hl = str(self)
        matches[hl] = sublocations[hl][0]

        sl = str(self.sl)
        matches[sl] = {}
        for sl_code in sublocations[sl]:
            matches[sl][sl_code] = self.sl.param_value_matches(
                sl_code, exclude_empty)

        ws = str(self.ws)
        matches[ws] = {}
        for ow_code in sublocations[ws]:
            matches[ws][ow_code] = self.ws.param_value_matches(
                ow_code, exclude_empty)

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
        self.sl_tags = SL_TAGS()
        self.sl_ti_h2go_tags = SL_TI_H2GO_TAGS()
        self.damo_pomp = DAMO_pomp()
        self.damo_stuw = DAMO_stuw()

    def __iter__(self):
        return iter((self.sl_tags, self.sl_ti_h2go_tags, self.damo_pomp,
                     self.damo_pomp))

    @property
    def param_matches(self) -> dict[str, dict[str, Param]]:
        '''
        Connect columns that share the same parameter
        '''
        return super().param_matches(self.sl_tags, self.sl_ti_h2go_tags)

    def param_value_matches(self, id: str, exclude_empty: bool
                            ) -> dict[str, dict[str, str]]:
        '''
        Connect values that share the same parameter at SL level
        '''
        return super().param_value_matches(
            self.param_matches, id, exclude_empty)


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
        self.ws_tags = WS_TAGS()
        self.ws_ti_h2go_tags = WS_TI_H2GO_TAGS()
        self.ws_validatie = WS_VALIDATIE()

    def __iter__(self):
        return iter((self.ws_tags, self.ws_ti_h2go_tags, self.ws_validatie))

    @property
    def param_matches(self) -> dict[str, dict[str, Param]]:
        '''
        Connect columns that share the same parameter
        '''
        return super().param_matches(self.ws_tags, self.ws_ti_h2go_tags)

    def param_value_matches(self, id: str, exclude_empty: bool
                            ) -> dict[str, dict[str, str]]:
        '''
        Connect values that share the same parameter OW level
        '''
        return super().param_value_matches(self.param_matches, id,
                                           exclude_empty)


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
        pass


class SL_TI_H2GO_TAGS(SpocFile):
    id = SLColumn('SL_CODE')
    type = Column('TYPE')
    shortname = Column('SHORTNAME')
    ti_code = Column('TI_CODE')
    h2go_locid = Column('H2GO_LOCID')

    param_bs = FileParam('BS_0', param='BS')
    param_tt = FileParam('TT_0', param='TT')
    param_sh = FileParam('SH_0', param='SH')
    param_sd = FileParam('SD_0', param='SD')
    param_mwar = FileParam('MWAR_0', param='MWAR')
    param_qb = FileParam('Q_B_0', param='QB')
    param_od = FileParam('OD_0', param='OD')
    param_gkz = FileParam('GKZ_0', param='GKZ')
    param_pf = FileParam('PF_0', param='PF')
    param_a = FileParam('A_0', param='A')
    param_so = FileParam('SO_0', param='SO')

    handh = Column('HANDH_0')
    commentaar = Column('_COMMENTAAR')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        pass

    def construct_param(
            self,
            id: SLColumn | str,
            param: FileParam | str
            ) -> str | float:
        locid = self.field(id, self.h2go_locid)
        mptid = self.field(id, param)
        if not any(pd.isna(v) for v in (locid, mptid)):
            return '_'.join(str(v) for v in (locid, mptid))
        return np.nan


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
        pass


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
        pass


class WS_TI_H2GO_TAGS(SpocFile):
    naam = Column('NAAM')
    id = WSColumn('OW_CODE')
    fewsparam = Column('FEWS_PARAM')
    ti_code = Column('TI_CODE')
    h2go_locid = Column('H2GO_LOCID')

    param_hm = FileParam('H2GO_MEETPUNTID', param='HM')
    param_qm = FileParam('H2GO_Q', param='QM')
    param_hmhand = FileParam('H2GO_HANDMEETPUNTID', param='HMHAND')

    comment = Column('COMMENT')
    gecontroleerd = Column('GECONTROLEERD')

    def __init__(self):
        pass

    def construct_param(
            self,
            id: WSColumn | str,
            param: FileParam | str
            ) -> str | float:
        locid = self.field(id, self.h2go_locid)
        mptid = self.field(id, param)
        if not any(pd.isna(v) for v in (locid, mptid)):
            return '_'.join(str(v) for v in (locid, mptid))
        return np.nan


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
        pass
