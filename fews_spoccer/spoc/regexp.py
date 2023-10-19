iwa_tag = (
    r'''(?P<marker1>.*)?'''                             # optional group1
    r'''(?P<prefix>~SCX)\.'''                           # tag prefix
    r'''(?P<tag_type>~Watersysteem.Objecten)\.'''       # tag type prefix
    r'''(?P<area>.*)\.'''                               # area
    r'''(?P<name>.*)\.Tags\.'''                         # object trivial name
    r'''(?P<optional>.*)NL\*09\*'''                     # optional group Tags.?
    r'''(?P<legger_code>[0-9]{6}\s)'''                  # object's db name
    r'''(?P<type>.*)\.'''                               # object's type
    r'''(?P<param>.*)\.'''                              # object's identifier
    r'''(?P<suffix>Historic)'''                         # tag suffix
    r'''(?P<marker2>.*)?'''                             # optional group2
)

pbh_tag = (
    r'''(?P<marker1>.*)?'''                             # optional group1
    r'''(?P<prefix>~SCX)\.'''                           # tag prefix
    r'''(?P<tag_type>Pbh)\.'''                          # tag type prefix
    r'''(?P<area>.*)\.'''                               # area
    r'''(?P<name>.*)\.'''                               # object's db name
    r'''(.*)\.'''                                       # not matched/remains
    r'''(?P<suffix>Historic)'''                         # tag suffix
    r'''(?P<marker2>.*)?'''                             # optional group2
)

avic_tag = (
    r'''(?P<marker1>.*)?'''                             # optional group1
    r'''(?P<prefix>~SCX)\.'''                           # tag prefix
    r'''(?P<tag_type>Applicatiebeheer\.~Koppelingen\.AvicDataloggers)\.'''
                                                        # tag type prefix
    r'''(?P<name>.*)\.'''                               # object trivial name
    r'''(?P<param>Niveau)\.'''                          # object's identifier
    r'''(?P<suffix>Historic)'''                         # tag suffix
    r'''(?P<marker2>.*)?'''                             # optional group2
)

vaarweg_tag = (
    r'''(?P<marker1>.*)?'''                             # optional group1
    r'''(?P<prefix>~SCX)\.'''                           # tag prefix
    r'''(?P<tag_type>~?Vaarwegen.Objecten)\.'''         # tag type prefix
    r'''(?P<name>.*)\.Tags\.'''                         # object trivial name
    r'''(('''                                           # optional group 1
    r'''(NL\*09\*)'''                                   # unnamed optional 1
    r'''(?P<legger_code>[0-9]{6})'''                    # object's db name
    r'''(.*)'''                                         # unnamed optional 2
    r''')|(.*))\.'''                                    # optional group 2
    r'''(?P<suffix>Historic)'''                         # tag suffix
    r'''(?P<marker2>.*)?'''                             # optional group2
)
