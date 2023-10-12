import pandas as pd

from .spocfile import SpocFile


class Column:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.name


class ID(Column):
    def __init__(self, id):
        super().__init__(id)


class Param(Column):
    def __init__(self, name, param):
        super().__init__(name)
        self.param = param


class HL(SpocFile):
    object_id = Column('OBJECTID')
    id = pid = ID('CODE')
    naam = Column('NAAM')
    types = Column('TYPES')
    shortname = Column('SHORTNAME')
    icon = Column('ICON')
    tooltop = Column('TOOLTIP')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    namespace = Column('NAMESPACE')
    x = Column('X')
    y = Column('Y')
    commentaar = Column('COMMENTAAR')
    area = Column('DS_GBD')

    _validation_rules = ['unique_ids']

    def __init__(self):
        self.sl = SL()
        self.ws = WS()

    def __iter__(self):
        return iter((self, self.sl, self.ws))

    def sublocations(self, id: str) -> dict[str, pd.DataFrame]:
        return {str(i): i.ids_by_pids(id) for i in self}


class SL(SpocFile):
    objectid = Column('OBJECTID')
    id = ID('CODE')
    name = Column('NAAM')
    type = Column('TYPE')
    area = Column('GEBIED')
    shortname = Column('SHORTNAME')
    icon = Column('ICON')
    tooltip = Column('TOOLTIP')
    fotoid = Column('Foto_id')
    pid = Column('PARENTLOCATIONID')
    hbov = Column('HBOV')
    hben = Column('HBEN_PS')
    hbovps = Column('HBOV_PS')
    hbenps = Column('HBEN_PS')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    namespace = Column('NAMESPACE')
    x = Column('X')
    y = Column('Y')
    commentaar = Column('COMMENTAAR')

    def __init__(self):
        self.sl_tags = SL_TAGS()
        self.sl_ti_h2go_tags = SL_TI_H2GO_TAGS()
        self.damo_pomp = DAMO_pomp()
        self.damo_stuw = DAMO_stuw()

    def __iter__(self):
        return iter((self.sl_tags, self.sl_ti_h2go_tags, self.damo_pomp,
                     self.damo_pomp))


class WS(SpocFile):
    id = ID('ï»¿CODE')
    naam = Column('NAAM')
    type = Column('TYPE')
    shortname = Column('SHORTNAME')
    area = Column('GEBIED')
    icon = Column('ICON')
    tooltip = Column('TOOLTIP')
    objectbegin = Column('OBJECTBEGI')
    objecteind = Column('OBJECTEIND')
    namespace = Column('NAMESPACE')
    x = Column('X')
    y = Column('Y')
    pid = Column('PARENTLOCATIONID')
    commentaar = Column('COMMENTAAR')
    scx_lcode = Column('SCX_Lcode')

    def __init__(self):
        self.ws_tags = WS_TAGS()
        self.ws_ti_h2go_tags = WS_TI_H2GO_TAGS()
        self.ws_validatie = WS_VALIDATIE()

    def __iter__(self):
        return iter((self.ws_tags, self.ws_ti_h2go_tags, self.ws_validatie))


class SL_TAGS(SpocFile):
    shortname = Column('SHORTNAME')
    id = ID('CODE')
    locationid = Column('LOCATIONID')
    source = Column('SOURCE')

    param_bs = Param('TAG_CGOO_BS', 'bs')
    param_tt = Param('TAG_CGOO_TT', 'tt')
    param_sh = Param('TAG_CGOO_SH', 'sh')
    param_sd = Param('TAG_CGOO_SD', 'sd')
    param_mwar = Param('TAG_CGOO_MWAR', 'mwar')
    param_qb = Param('TAG_CGOO_Q_berekening', 'qb')
    param_od = Param('TAG_CGOO_OPEN_DICHT', 'od')
    param_gkz = Param('TAG_CGOO_GKZ', 'gkz')
    param_pf = Param('TAG_CGOO_FREQ', 'pf')
    param_a = Param('TAG_CGOO_A', 'a')
    param_so = Param('TAG_CGOO_SO', 'so')

    tag_cgoo_q_meting = Column('TAG_CGOO_Q_meting')
    tag_cgoo_niveau_put = Column('TAG_CGOO_NIVEAU_PUT')
    tag_cgoo_qin = Column('TAG_CGOO_QIN')

    gecontroleerd = Column('GECONTROLEERD')
    tag_cgoo_bs_unit = Column('TAG_CGOO_BS_UNIT')
    tag_cgoo_q_berekening_unit = Column('TAG_CGOO_Q_berekening_UNIT')

    def __init__(self):
        pass

    @property
    def params(self):
        params = {}
        for k, v in self.__class__.__dict__.items():
            if k.startswith('param_'):
                param = k.split('_')[-1]
                params.update({param: v})
        return params


class SL_TI_H2GO_TAGS(SpocFile):
    id = 'SL_CODE'
    type = 'TYPE'
    shortname = 'SHORTNAME'
    ti_code = 'TI_CODE'
    h2go_locid = 'H2GO_LOCID'

    param_bs = 'BS_0'
    param_tt = 'TT_0'
    param_sh = 'SH_0'
    param_sd = 'SD_0'
    param_mwar = 'MWAR_0'
    param_qb = 'Q_B_0'
    param_od = 'OD_0'
    param_gkz = 'GKZ_0'
    param_pf = 'PF_0'
    param_a = 'A_0'
    param_so = 'SO_0'

    handh = 'HANDH_0'
    commentaar = '_COMMENTAAR'
    gecontroleerd = 'GECONTROLEERD'

    def __init__(self):
        pass


class DAMO_pomp(SpocFile):
    def __init__(self):
        pass


class DAMO_stuw(SpocFile):
    def __init__(self):
        pass


class WS_TAGS(SpocFile):
    id = 'LOCATIONID'
    source = 'SOURCE'

    param_hm = 'TAG_CGOO_MNAP'
    param_qm = 'TAG_CGOO_Q'

    gecontroleerd = 'GECONTROLEERD'

    def __init__(self):
        pass


class WS_TI_H2GO_TAGS(SpocFile):
    naam = 'NAAM'
    id = 'OW_CODE'
    fewsparam = 'FEWS_PARAM'
    ti_code = 'TI_CODE'
    h2go_locid = 'H2GO_LOCID'

    param_hm = 'H2GO_MEETPUNTID'
    param_qm = 'H2GO_Q'
    param_hmhand = 'H2GO_HANDMEETPUNTID'

    comment = 'COMMENT'
    gecontroleerd = 'GECONTROLEERD'

    def __init__(self):
        pass


class WS_VALIDATIE(SpocFile):
    def __init__(self):
        pass
