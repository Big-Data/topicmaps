# -*- coding: utf-8 -*-
#
# Donated to the public domain by Lars Heuer - <heuer[at]semgia.com>
#
import re
from datetime import date
from StringIO import StringIO
from urllib import quote

_NAMESPACES = {
    'subj': 'http://psi.metaleaks.org/cablegate/subject-tag/',
    'org': 'http://psi.metaleaks.org/cablegate/org-tag/',
    'program': 'http://psi.metaleaks.org/cablegate/program-tag/',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

def generate_ctm(fileobj):
    """\
    
    `fileobj`
        A file object.
    """
    def write_tags(s, seen_tags, dupl_tags, prefix, header=None):
        if header:
            fileobj.write("""\
#
#-- %s
#
""" % header)
        for sid, tag, name in _get_sid_tag_name(s, prefix):
            if sid in seen_tags:
                fileobj.write('# CAUTION: Duplicate\n')
                if sid not in dupl_tags:
                    dupl_tags.append(sid)
            else:
                seen_tags.append(sid)
            fileobj.write(u'%s - "%s"; - dc:title: "%s".\n\n' % (sid, tag, name))
    fileobj.write(u"""\
#
# ==============
# Cablegate TAGS
# ==============
#
#
# Description:  This topic map assigns names to TAGS
#
# License:      Public Domain
#
# Source:       <https://cabletags.wordpress.com/>
#
# Date:         2011-01-04
#
# Modified:     %s
# 

#
# Prefixes
#
%s


""" % (date.today().isoformat(), '\n'.join(['%prefix ' + k + '<' + v + '>' for k, v in _NAMESPACES.iteritems()]))    )
    seen_tags = []
    dupl_tags = []
    write_tags(SUBJECT_TAGS, seen_tags, dupl_tags, prefix='subj', header='Subject Tags')
    write_tags(ORG_TAGS, seen_tags, dupl_tags, prefix='org', header='Organization Tags')
    write_tags(PROGRAM_TAGS, seen_tags, dupl_tags, prefix='program', header='Program Tags')
    if dupl_tags:
        fileobj.write('\n\n# Duplicates: %r\n' % dupl_tags)


def _get_sid_tag_name(s, prefix):
    """\
    Returns a tuple (sid, tag, name) where "sid" is either an IRI or a QName.

    `s`
        The string to read the tags/names from (tag <tab> name).
    """
    for tag, name in _get_tag_name(s):
        path = quote(tag).replace('/', '%2F')
        if path == tag:
            sid = u'%s:%s' % (prefix, tag)
        else:
            sid = u'<%s/%s>' % (_NAMESPACES.get('prefix'), path)
        yield sid, tag, name


_TAG_NAME_PATTERN = re.compile(ur'^([A-Za-z0-9&/ _-]+)(?:[ \t]+)(.+)$', re.UNICODE)
_WS_NORMALIZER_PATTERN = re.compile(r'[ ]+')

def _get_tag_name(s):
    """\
    Returns a tuple (tag, name)
    
    `s`
        The string to read the tags/names from (tag <tab> name).
    """
    for l in StringIO(s):
        tag, name = _TAG_NAME_PATTERN.match(l).groups()
        tag = tag.strip().upper()
        tag = _WS_NORMALIZER_PATTERN.sub(' ', tag)
        yield tag, name

#
# Source: <https://cabletags.wordpress.com>
# 
# 2010-12-29
#

SUBJECT_TAGS = u"""\
AADP 	Automated Data Processing
ABLD 	Buildings and Grounds
ABUD 	Budget Services and Financial Systems
ACOA 	Communication Operations and Administration
ACKM 	COMSEC Key Management
ADCO 	Diplomatic Courier Operations
ADPM 	Diplomatic Pouch and Mail
AEMR 	Emergency Planning and Evacuation
AFIN 	Financial Management
AFSI 	Foreign Service Institute
AFSN 	Foreign Service National Personnel
AGAO 	General Accounting Office
AINF 	Information Management Services
AINR 	INR Program Administration
AINT 	Internet Administration
ALOW 	Allowances
AMED 	Medical Services
AMGT 	Management Operations
AMTC 	Telecommunications Equipment Maintenance
ANET 	Communications, Circuits, and Networks
AODE 	Employees Abroad
AOMS 	Office Management Specialist Issues
AORC 	International Organizations and Conferences
APCS 	Personal Computers
APER 	Personnel
ASCH 	U.S. Sponsored Schools
ASEC 	Security
ASIG 	Inspector General Activities
BBSR 	Business Services Reporting
BEXP 	Trade Expansion and Promotion
BMGT 	FCS Management Operations
BTIO 	Trade and Investment Opportunities
CASC 	Assistance to Citizens
CFED 	Federal Agency Services
CJAN 	Judicial Assistance and Notarial Services
CLOK 	Visa Lookout
CMGT 	Consular Administration and Management
CPAS 	Passport and Citizenship
CVIS 	Visas
EAGR 	Agriculture and Forestry
EAID 	Foreign Economic Assistance
EAIR 	Civil Aviation
ECON 	Economic Conditions
ECPS 	Communications and Postal Systems
EFIN 	Financial and Monetary Affairs
EFIS 	Commercial Fishing and Fish Processing
EIND 	Industry and Manufacturing
EINT 	Economic and Commercial Internet
EINV 	Foreign Investments
ELAB 	Labor Sector Affairs
ELTN 	Land Transportation
EMIN 	Minerals and Metals
ENRG 	Energy and Power
EPET 	Petroleum and Natural Gas
ETRD 	Foreign Trade
ETTC 	Trade and Technology Controls
EWWT 	Waterborne Transportation
MARR 	Military and Defense Arrangements
MASS 	Military Assistance and Sales
MCAP 	Military Capabilities
MNUC 	Military Nuclear Applications
MOPS 	Military Operations
ODIP 	U.S. Diplomatic Representation
OEXC 	Educational and Cultural Exchange Operations
OFDP 	Foreign Diplomats and Foreign Missions
OIIP 	International Information Programs
OPDC 	Diplomatic Correspondence
OPRC 	Public Relations and Correspondence
OREP 	U.S. Congressional Travel
OSCI 	Science Grants
OTRA 	Travel
OVIP 	Visits and Travel of Prominent Individuals and Leaders
PARM 	Arms Controls and Disarmament
PBTS 	National Boundaries, Territories, and Sovereignty
PGOV 	Internal Governmental Affairs
PHSA 	High Seas Affairs
PHUM 	Human Rights
PINR 	Intelligence
PINS 	National Security
PNAT 	National Independence
PREF 	Refugees
PREL 	External Political Relations
PROP 	Propaganda and Psychological Operations
PTER 	Terrorists and Terrorism
SCUL 	Cultural Affairs
SENV 	Environmental Affairs
SMIG 	Migration
SNAR 	Narcotics
SOCI 	Social Conditions
TBIO 	Biological and Medical Science
TINT 	Internet Technology
TNGD 	Engineering Research and Development
TPHY 	Physical Sciences
TRGY 	Energy Technology
TSPA 	Space Activities
TSPL 	Science and Technology Policy
"""

PROGRAM_TAGS = u"""\
KACT 	Strategic Arms Control (ACS) Treaties
KAWC 	Atrocities and War Crimes
KBCT 	Arab League Boycott
KCCP 	Classified Connectivity Deployment Program
KCFE 	Conventional Armed Forces in Europe
KCIP 	Critical Infrastructure Protection
KCIS 	Posts Classified Information Handling
KCOG 	Continuity of the Federal Government
KCOM 	Chief of Mission
KCOR 	Corruption and Anti-Corruption
KCRM 	Criminal Activity
KCRS 	Coordinator for Reconstruction and Stabilization
KCSY 	Consular System
KDEM 	Democratization
KDRG 	Detainee Repatriation from Guantanamo Bay
KEAI 	Enterprise for the Americas Initiative
KECF 	The U.S. Africa Economic Cooperation Forum
KEMS 	Electronic Messaging Systems
KESS 	Emergency Security Supplemental
KFAM 	Foreign Affairs Manual
KFLO 	Family Liaison
KFLU 	Avian and Pandemic Influenza Activities
KFPC 	Foreign Policy Trade Controls and East/West Trade
KFRD 	Fraud Prevention Programs
KFSC 	Financial Service Center Operations
KGCN 	Government to Government Claims Negotiations
KGHA 	Greater Horn of Africa Initiative
KGHG 	Global Climate Change
KGIC 	Global Initiative to Combat Nuclear Terrorism
KGIT 	Global Information Technology Modernization Program
KGLB 	Global Learning and Observations to Benefit the Environment (GLOBE)
KHDP 	Humanitarian Demining Program
KHIV 	Emerging Infectious Diseases and HIV/AIDS Program
KHLS 	Homeland Security
KICA 	International Cooperative Administrative Support Services
KICR 	International Coral Reef Initiative
KICT 	Iran-U.S. Claims Tribunal
KIDE 	Investment Disputes and Property Expropriations
KIMT 	Information Management Training
KIPR 	Intellectual Property Rights
KIRC 	Information Resource Centers
KIRF 	International Religious Freedom
KISL 	Islamic Issues
KJUS 	Administration of Justice
KLBO 	Information Resource Management Liaison Office to Overseas Buildings Operations
KLIG 	Foreign Litigation
KLSO 	Language Support Operations
KMCA 	Millennium Challenge Account
KMDR 	Media Reaction Reporting
KMFO 	Multinational Force Observers
KMPI 	Middle East Partnership Initiative
KMRS 	Rightsizing the U.S. Government’s Overseas Presence
KMSG 	Marine Security Guard Program
KNAR 	Nazi Assets and Restitution
KNEI 	Northern Europe Initiative (NEI)
KNEP 	Nonexpendable Property Application (NEPA)
KNET 	Department of State Telecommunications Network (DOSTN) Program
KNNP 	Nuclear Non- Proliferation
KNSD 	North-South Dialogue
KOCI 	Children’s Issues
KOGL 	Open Source and Gray Literature
KOLY 	Olympic Games Reporting
KOMC 	Export Control of Defense Articles and Defense Services
KONP 	OpenNet Plus Program
KPAL 	Palestinian Affairs
KPAM 	Property Accountability Management
KPAO 	Public Affairs Office
KPAP 	Overseas Presence Advisory Panel (OPAP)
KPDC 	Protected Digital Copier
KPIN 	Political Internationals
KPIR 	Maritime Piracy and Armed Robbery Against Ships
KPKO 	United Nations Peacekeeping Operations
KPLS 	Polls, Survey Research and Focus Groups
KPMP 	Patch Management Program
KPOW 	Prisoners of War/Missing in Action
KPRV 	Privatization
KPWR 	Power Support Program
KQDD 	Quadrennial Diplomacy and Developments Review
KRAD 	Radioactive Contamination of the Environment
KREC 	Reciprocity
KRIM 	Regional Information Management Centers
KRVC 	Research Vessel Clearances
KSAC 	Security Advisory Council
KSAF 	Safety Program
KSCA 	Science Counselors and Attachés
KSEI 	Southeast European Cooperative Initiative
KSEO 	Security Engineering Operations
KSIP 	IT Skills Incentive Program
KSLG 	Secure Logistics
KSPR 	Strategic, Performance and Resource Planning
KSRK 	Visas Shark Communication
KSTC 	Strategic Trade and Technology Controls
KSTT 	State Transition Team
KSUM 	Summit Meetings
KTDB 	National Trade Data Bank
KTEX 	Textiles
KTFN 	Terrorism Finance Traffic
KTIA 	Treaties and International Agreements
KTIP 	Trafficking in Persons
KTSD 	Trilateral Strategic Dialogue
KUNC 	United Nations Compensation Commission
KUNR 	UN Reform
KVIR 	Computer Virus and/or Anti-Virus Program
KVPR 	Visas VIPER Communications
KWBG 	West Bank and Gaza
KWIR 	Wireless
KWMN 	Women Issues
KWPA 	Worldwide Property Accountability
KWWW 	World Wide Web Site
"""

#
# Removed acc. to <http://www.state.gov/documents/organization/89258.pdf>
#   AID 	International Cooperation Administration
#   BQG 	Bonn Quadripartite Group
#   BQG 	Bonngroup
#   CDG 	Conference of Committee on Disarmament
#   CEP 	Civil Emergency Planning Committee Senior Civil Emergency Planning Committee
#   CEMA 	CMEA
#   CEMA 	COMECON
#   CITEL 	Inter-American Telecommunications Commission
#   Colombo Plan 	CPCTC
#   ECA 	UN Economic Commission for Africa
#   ECA 	Economic Commission for Africa (UN)
#   EUN 	Communaute Economique Europeene
#   EUN 	European Common Market
#   EUN 	European Communities
#   EUN 	European Economic Community
#   EUN 	European Union
#   EUN 	Marche Commun European
#   EUN 	European Economic Community AKA European Common Market
#   SWAPO 	Southwest Africa Peoples’ Organization
#   UNPUOS 	UN Committee on Peaceful Uses of Outer Space & UN Outer Space Committee
#   UNPUOS 	UN Outer Space Committee
#   UNTC 	UN Trusteeship Council
#   UNTERR 	UN Committee on International Terrorism
#   UNTERR 	Terrorism Committee (UN)
#   WCL 	International Federation of Christian World Confederation of
#   WCL 	International Federation of Christian Trade Unions
#   WCL 	World Confederation of Labor
ORG_TAGS = u"""\
AAA 	American Automobile Association
AAFLI 	Asian American Free Labor Institute
AAI 	African American Institute
AALC 	African American Labor Center
ABA 	American Bar Association
ABC 	American Broadcasting Company
ABMC 	American Battle Monuments Commission
ACABQ 	UN Advisory Committee on Administration and Budget Questions
ACTU 	Australian Labor Union
ADB 	Asian Development Bank
ADB-1 	Association for the Advancement of International Education
ADF 	African Development Foundation
ADPSEC 	Automatic Data Processing Security
AEC 	Atomic Energy Commission
AEDF 	Asian Economic Development Fund
AER LINGUS 	Irish Airline
AEROFLOT 	Soviet Airline
AEROLINEAS ARGENTINAS 	Argentine Airline
AEROPERU 	National Airline of Peru
AFDB 	African Development Bank
AFDF 	African Development Fund
AFL-CIO 	American Federation of Labor-Congress of Industrial Organizations
AFP 	Agence France Press
AFSA 	American Foreign Service Association
AGR 	Department of Agriculture
AI 	Amnesty International
AID 	Agency for International Development
AIFLD 	American Institute for Free Labor Development
AKB 	Allied Kommandatura Berlin
AL 	Arab League
AL-1 	Arab League
ALIA 	Royal Jordanian Airline
Alitalia 	Italian Airline
ALP 	Australian Labor Party
AMAL 	Movement of the Deprived (Sh’a Muslim Militia Organization)
AMAX 	American Metals Climax Inc
AMCHAMS 	American Chambers of Commerce
AMOCO 	American Oil Company
ANC 	African National Congress
ANZUS 	Australia, New Zealand and US Council
AP 	Associated Press
APAG 	Atlantic Policy Advisory Group
APCAC 	Asian Pacific Council of American Chambers of Commerce
APECO 	Asia Pacific Economic Cooperation
ARAMCO 	Arabian American Oil Company
ARC 	American Red Cross
ARCO 	Atlantic Richfield Oil Company
ARDE 	Revolutionary Democratic Alliance
ARENA 	Political Party in El Salvador
ARIANA 	Afghan Airline
ASALA 	Armenian Secret Army
ASEAN 	Association of Southeast Asian Nations
ASPAC 	Asian and Pacific Council
AT&T 	American Telephone & Telegraph
ATA 	Atlantic Treaty Association
AU-1 	African Union
AUB 	American University in Beirut
AUCCTU 	All Union Central Council of Trade Unions (USSR)
AVENSA 	Aerovias Venezolanas
AVIANCA 	Aerovias Nacionales De Colombia
BASC 	Berlin Air Safety Center
BBC 	British Broadcasting Company
BBG 	Broadcasting Board of Governors
BDC 	Berlin Document Center
BENDIX 	Bendix Corporation
BIE 	Bureau of International Expositions
BIS 	Bank of International Settlements
BLS 	Bureau of Labor Statistics
BOS 	Southern Opposition Block
BP 	British Petroleum Company
BP-1 	British Petroleum Company
BQG 	Berlin Quadripartite Group
Bundesbank 	Central Bank of the FRG
BWIA 	British West Indies Airline
CAA 	British Civil Aviation Authority
CAAC 	Civil Aviation Authority for China
CACM 	Central American Common Market
CAPC 	Civil Aviation Planning Committee (NATO)
CARE 	Cooperative for American Relief Everywhere, Inc
CBC 	Canadian Broadcasting Corporation
CBS 	Columbia Broadcasting System
CCC-1 	Commodity Credit Corporation
CCC-3 	Customs Cooperation Council
CCD 	Committee on Disarmament
CCIR 	International Radio Consultative Committee
CCITT 	International Telegraph and Telephone Consultative Committee
CCMS 	Committee on the Challenges of Modern Society
CCNAA 	Coordinating Council for North American Affairs
CCUS 	Chamber of Commerce of the US
CDB 	Caribbean Development Bank
CDC 	Communicable Diseases Center
CDG 	Committee on Disarmament
CDI 	Christian Democratic International
CDU 	Christian Democratic Union
CEA 	Council of Economic Advisers
CEAC 	Committee on European Airspace Coordination
CEC 	Commission of the European Communities
CEMA 	Council for Mutual Economic Assistance
CEP 	Civil Emergency Planning Committee
CEQ 	Council on Environmental Quality
CIA 	Central Intelligence Agency
CIEC 	Inter-American Council on Education Science and Culture
CIL 	Central Identification Lab
CIME 	Committee on Investments and Multi-National Enterprise
CIP 	Council on International Programs
CIPEC 	Intergovernmental Council of Copper Exporting Countries
CIS 	Commonwealth of Independent States
CITEL 	Inter-American Telecommunications Commissions
CITIBANK 	First National City Bank of New York
COE 	Council of Europe
Colombo Plan 	Colombo Plan Council for Technical Cooperation in South and Southeast Asia
COM 	Department of Commerce
COMIBOL 	Bolivian National Mining Corporation or Corporacion Minera De Bolivia
CONDECA 	Central American Defense Council
CONOCO 	Continental Oil Company
CONTRIB 	UN Committee on Contributions
COSEP 	Superior Council of the Private Sector Groups in Nicaragua
CPC 	UN Committee for Program and Coordination
CPSU 	Communist Party in the USSR
CRS 	Catholic Relief Services
CSIS 	Center for Strategic and International Studies
CSTP 	Committee for Scientific and Technical Personnel
CSU 	Christian Social Union
CTM 	Customs
CWC 	Chemical Weapons Convention
CWS 	Church World Service
DAC 	Development Assistance Committee (OECD)
DC 	Christian Democratic Party in Italy
DCA 	Defense Communication Agency
DCI 	Defense Capabilities Initiative
DEA 	Drug Enforcement Administration
DHS 	Department of Homeland Security
DIA 	Defense Intelligence Agency
DJP 	Ruling Democratic Justice Party
DOD 	Department of Defense
DOE 	Department of Energy
DOT 	Department of Transportation
DPC 	Defense Planning Commission
DPP 	Democratic Progressive Party
DPR 	Office of Policy and Resources
EAC 	East African Community
EAL 	Ethiopian Airlines
EALG 	East Asian Liaison Group
EAPC 	Euro-Atlantic Partnership Council
EBRD 	European Bank for Reconstruction and Development
ECA 	Economic Commission for Africa (UN), UN Economic Commission for Africa
ECAC 	European Civil Aviation Conference
ECDC 	Economic Cooperation and Development Comt
ECE 	UN Economic Commission for Europe
ECG 	Energy Coordinating Group
ECLAC 	CEPAL, UN Economic Commission for Latin America and the Caribbean
ECMT 	European Conference of Ministers of Transport
ECOSOC 	UN Economic and Social Council, UNECOSOC
ECOWAS 	Economic Community of West African States
ECWA 	UN Economic Commission for Western Asia
ED 	Department of Education
EDC 	Export Development Corporation
EDRC 	Economic and Development Review Committee in OECD
EDU 	European Democratic Union
EEOC 	Equal Employment Opportunity Commission
EFTA 	European Free Trade Association AKA Outer Seven AKA The Seven
EL AL 	Israeli Airlines
ELF 	Eritrean Liberation Front
ELN 	Bolivian National Liberation Army
EP 	European Parliament
EPA 	Environmental Protection Agency
EPC 	Economic Policy Committee (OECD)
ESA 	European Space Agency
ESCAP 	UN Economic and Social Commission for Asia and Pacific
ESDI 	European Security and Defense Identity
ETA 	Basque Terrorist Group
EUCOM 	European Command
EUN 	European Atomic Energy Community
EUROCONTROL 	European Organization for the Safety of Air Navigation
EXIM 	Export Import Bank of US
FAA 	Federal Aviation Administration
FAO 	Food and Agriculture Organization of the UN
FAPC 	Food and Agriculture Planning Committee
FAPLA 	Forcas Armadas Para A Liberacao De Angola
FARC 	Fuerzas Armadas Revolucionaria
FAS 	Foreign Agriculture Service (Dept. of Agriculture)
FBI 	Federal Bureau of Investigation
FBIS 	Foreign Broadcast Information Service
FCC 	Federal Communications Commission
FCIA 	Federal Credit Insurance Association
FCSC 	Foreign Claims Settlement Commission of the US
FDA 	Food and Drug Administration (HHS)
FDIC 	Federal Deposit Insurance Corp.
FDN 	Democratic Revolutionary Front in El Salvador
FDR 	Guerrilla Group in El Salvador
FEMA 	Federal Emergency Management Administration
FHWA 	Federal Highway Administration
FINNAIR 	National Airline of Finland
FLN 	Algerian National Liberation Front AKA National Army of Liberation (Algeria)
FMC 	Federal Maritime Commission
FMLN 	Farabundo Marti Liberacion Nacional
FNLA 	National Front for the Liberation of Angola
FPC 	Federal Power Commission
FRB 	Board of Governors of the Federal Reserve System AKA Federal Reserve Board
FRELIMO 	Leading Angolan Political Party
FSCADP 	FSC Paris ADP Center
FSLN 	Sandinistas National Liberation Front
FTC 	Federal Trade Commission
FTUI 	Free Trade Union Institute
FWS 	Fish and Wildlife Service
G-77 	Group of Seventy-Seven
G-8 	Group of Eight
GAO 	General Accounting Office
GATT 	General Agreement on Tariffs and Trade
GCC 	Gulf Cooperation Council
General Motors 	GM
GM-1 	General Motors
GPO 	Government Printing Office
GREENS 	Green Party
GSA 	General Services Administration
HCOPIL 	Hague Conference on Private Intl Law
HHS 	Department of Health and Human Services
HKA 	Hong Kong Airways
HUD 	Department of Housing and Urban Development
IACI 	Inter-American Children’s Institute
IACW 	Inter-American Commission of Women
IADB 	Inter-American Defense Board
IAEA 	International Atomic Energy Agency
IA-ECOSOC 	Inter-American Economic and Social Council
IAF 	Inter-American Foundation
IAHRC 	Inter-American Human Rights Commission
IAII 	Inter-American Indian Institute
IAJC 	Inter-American Juridical Committee (OAS)
IARC 	International Agency for Research on Cancer
IATA 	International Air Transport Association
IATTC 	Inter-American Tropical Tuna Commission
IBC 	International Boundary Commission United States and Canada
IBM 	International Business Machines
IBPCA 	International Bureau of the Permanent Court of Arbitration
IBPCT 	International Bureau for the Publication of Customs Tariffs
IBRD 	International Bank for Reconstruction and Development, a Specialized Agency of the UN
IBWC 	International Boundary and Water Commission United States and Mexico
IBWM 	International Bureau of Weights and Measures
ICAC 	International Cotton Advisory Committee
ICAF 	Industrial College of the Armed Forces
ICAO 	International Civil Aviation Organization, a specialized agency of the UN
ICBL 	The International Campaign to Ban Landmines
ICC 	Interstate Commerce Commission
ICCAT 	International Convention for the Conservation of Atlantic Tunas
ICCROM 	International Center for the Study of the Preservation and Restoration of Cultural Property
ICES 	International Council for the Exploration of the Sea
ICFTU 	International Confederation of Free Trade Unions
ICJ 	International Court of Justice
ICMC 	International Catholic Migration Commission
ICO 	International Coffee Organization
ICO-1 	International Cocoa Organization
ICRC 	International Committee of the Red Cross
ICSC 	Interim Committee on Communication Satellites
ICTR 	International Criminal Tribunal for Rwanda
ICTY 	International Criminal Tribunal for the former Yugoslavia
IDA 	International Development Association Administered by the IBRD
IDB 	Inter-American Development Bank AKA Banco Interamericano de Desarollo in Washington, not a UN activity
IEA 	International Energy Agency
IFAD 	Fund for Agricultural Development, International Fund for Agriculture Development
IFC 	International Finance Corporation in Washington, an affiliate of IBRD but a separate legal entity
IFRB 	International Frequency Registration Board
IFRC 	International Federation of Red Cross and Red Crescent Societies
IHB 	International Hydrographic Bureau
IIC 	International Institute for Cotton
IICA 	Inter-American Institute of Agriculture
IJC 	International Joint Commission U.S.-Canada
IJO 	International Jute Organization
ILA 	International Law Association
ILC 	International Law Commission
ILO 	International Labor Organization—specialized agency of the UN
ILZSG 	International Lead and Zinc Study Group
IMC 	International Meteorological Committee
IMF 	International Monetary Fund in Washington—Related to the UN
IMH 	International Mission of Hope
IMO 	Intergovernmental Maritime Consultative Organization
INCB 	International Narcotics Control Board
INFCE 	International Nuclear Cycle Evaluation
INMARSAT 	International Maritime Satellite
INPFC 	International North Pacific Fisheries Commission
INRA 	National Institute for Agrarian Reform
INRO 	International Natural Rubber Organization
INS 	Immigration and Naturalization Service
INT 	Department of the Interior
INTELSAT 	International Telecomsatellite Consort
INTERPOL 	International Criminal Police Organization
IOC 	Intergovernmental Oceanographic Commission
IOLM 	International Organization for Legal Metrology
IOM 	International Organization for Migration
IOVW 	International Office of the Vine and Wine
IPDC 	International Program for Development of Communications
IPHC 	International Pacific Halibut Commission U.S. and Canada
IPU 	Interparliamentary Union
IRA 	Irish Republican Army
IRC 	International Rice Commission
IRC-2 	International Rescue Committee
IRC-3 	International Red Cross
IREX 	International Research and Exchange Board
IRS 	Internal Revenue Service
IRSG 	International Rubber Study Group
ISCON 	Islamic Conference
ISO 	International Sugar Organization
ISTA 	International Seed Testing Association
ITC 	International Trade Commission
ITT 	International Telephone and Telegraph Company
ITTO 	International Tropical Timber Organization
ITU 	International Telecommunication Union—specialized agency of the UN
IUCNNR 	International Union for the Conservation of Nature and Natural Resources
IWBC 	International Boundary and Water Commission United States and Mexico
IWC-1 	International Whaling Commission
IWC-2 	International Wheat Council
IWSG 	International Wool Study Group
IYC 	International Youth Conference
JAL 	Japan Air Lines
JAT 	Yugoslav Airline
JCIC 	Joint Compliance and Inspection Commission
JDL 	Jewish Defense League
JLP 	Jamaica Labor Party
JUS 	Department of Justice
KAL 	Korean National Airlines
KANU 	Kenya African National Union
KGB 	Soviet Intelligence Service
KLM 	Royal Dutch Airlines
KMT 	Kuomintang or Nationalist Party
KOC 	Kuwait Oil Company
KPNLF 	Khmer Peoples National Liberation Front
LAB 	Department of Labor
LBAR 	Board of Appellate Review
LDP 	Liberal Democratic Party
LOC 	Library of Congress
LOT 	Polish National Airlines
MAB 	Man and the Biosphere Program (The)
MARAD 	US Maritime Administration
MAS 	Military Agency for Standardization
MCG 	Mediterranean Cooperation Group (NATO)
MCLRS 	Maintenance of Certain Lights in the Red Sea
MEA 	Middle East Airlines
MFO 	Multinational Force Observers
MINURSO 	UN Mission for the Referendum in Western Sahara
MIR 	Leftist Revolutionary Movement in Bolivia
MNLF 	Mor National Liberation Front
MONUC 	UN Organization Mission in the Democratic Republic of the Congo
MPEAA 	Motion Picture Export Association of America
MPLA 	Popular Movement for the Liberation of Angola
MTCRE 	Missile Technology Control Regime
MTN 	Multilateral Trade Negotiations
NAA 	North Atlantic Assembly
NAC 	North Atlantic Council
NACB 	Nonaligned Coordinating Bureau
NAFO 	Northwest Atlantic Fisheries Organization
NAMSA 	NATO Management Supply Agency
NAS 	National Academy of Sciences (US)
NASA 	National Aeronautics and Space Admin
NASCO 	North Atlantic Salmon Conservation Organization
NATO 	North Atlantic Treaty Organization
NBC 	National Broadcasting Company
NBCCA 	National Bipartisan Comm on Central America
NBS 	National Bureau of Standards
NDR 	Nicaraguan Democratic Resistance
NDU 	National Defense University
NEB 	National Energy Board
NGA 	National Gallery of Art
NIAG 	NATO Industrial Advisory Group
NICSMA 	NATO Integrated Communications Systems
NIDA 	National Institute on Drug Abuse
NIH 	National Institute of Health
NIOC 	National Iranian Oil Company
NKDP 	New Korean Democratic Party
NMFS 	National Marine Fisheries Services
NNPC 	Nigerian National Petroleum Corp
NOAA 	National Oceanographic and Atmosphere Agency
NPC 	National Peoples Congress
NPFSC 	North Pacific Fur Seal Commission
NPG 	Nuclear Planning Group NATO
NRC-5 	National Research Council (US)
NSA 	National Security Agency
NSC 	National Security Council
NSF 	National Science Foundation
NTIA 	National Telecommunications and Information Administration
NTIS 	National Technical Information Service
NTSB 	National Transportation Safety Board
NTT 	Nippon Telegraph and Telephone Corp
NUC 	NATO-Ukraine Commission
NWC 	National War College
OAPEC 	Organization of Arab Petroleum Exporting Countries
OAS 	Organization of American States
OATU 	Organization of African Union Unity
OAU 	Organization of African Unity
OECD 	Organization for Economic Cooperation and Development in Paris
OECS 	Organization of Eastern Caribbean States
OIC-2 	International Olympic Committee
OIE 	International Office of Epizootics
OMB 	Office of Management and Budget Formerly Bureau of the Budget
OMSN 	Office of Micronesian Status Negotiations
OPEC 	Organization of Petroleum Exporting Countries
OPIC 	Overseas Private Investment Corporation
OPM 	Office of Personnel Management
ORIT-ICFTU 	Inter-American Regional Organization of the ICFTU, Organizacion Regional Interamericana de Trabajadores
OSCE 	Organization for Security and Cooperation in Europe
OSHA 	Occupational Safety and Health Administration
OSIA 	Onsight Inspection Agency
OVP 	Office of the Vice President
PAC 	Pan Africanist Congress
PAHO 	Pan American Health Organization in Washington
PAIGH 	Pan American Institute of Geography and History
PAL 	Philippine Airlines
PAN 	Partido Accion Nacional
PARCA 	Pan American Railway Congress Association in Buenos Aires
PBEIST 	Planning Board for European Inland Surface Transportation
PBOS 	Planning Board on Ocean Shipping
PBS 	Public Broadcasting System
PCC 	Panama Canal Commission
PCI 	Italian Communist Party
PDC 	Christian Democratic Party in El Salvador
PEMEX 	Petroleas Mexicanos
PETROBRAS 	Brazilian State Owned Oil Company
PFLP 	Popular Front for Liberation of Palestine
PFP 	Partnership for Peace (NATO)
Phalange Party 	Political Party in Lebanon
PHS 	Public Health Service
PIA 	Pakistani Airlines
PIARC 	Permanent International Association of Road Congresses
PICES 	North Pacific Marine Science Organization
PJC 	Permanent Joint Council, NATO-Russia
PKFK 	NATO Led Peacekeeping Forces in Kosovo
PLA 	Sudan Peoples’ Liberation Army
PLN 	National Liberation Front in Costa Rica
PLO 	Palestine Liberation Organization
PNC 	Palestinian National Council
PNDC 	Provisional National Defense Council
PNP 	Peoples National Party
PPD 	Party for Peace and Democracy
PPP 	Pakistan Peoples Party
PRI 	Partido Revolucionario Institucional
PSD 	Social Democratic Party in Portugal
PSI 	Italian Socialist Party
PSOE 	Spanish Socialist Workers’ Party
PUAS 	Postal Union of the Americas and Spain
QANTAS 	Qantas Empire Airways
RDP 	Reunification Democracy Party
RENAMO 	Resistencia Nacional Mocambicana
RFE 	Radio Free Europe
RL 	Radio Liberty
RRB 	Railroad Retirement Board
SAARC 	South Asian Association for Regional Cooperation
SAS 	Scandinavian Airlines System
SBA 	Small Business Administration
SCC 	Standing Consultative Commission
SCEPC 	Senior Civil Emergency Planning Committee
SDFCU 	State Department Federal Credit Union
SEC 	Securities and Exchange Commission
SELA 	Latin American Economic System
SFOR 	NATO Led Stabilization Forces in Bosnia-Herzegovina
SMI 	Smithsonian Institution
SOCINT 	Socialist International
SPC 	Secretariat of the Pacific Community
SPD 	Social Democratic Party in FRG and UK
SPF 	South Pacific Forum
SPLA 	Sudan Peoples’ Liberation Army
SPLM 	Sudan Peoples’ Liberation Movement
SSA 	Social Security Administration
SSOD 	Special Session on Disarmament (UN)
STAT 	UN Statistical Commission
SVC 	Special Verification Commission
SWAPO 	Southwest Africa Peoples Organization
TAPLINE 	Trans Arabian Pipeline Company
TDB 	Trade and Development Board
TGC 	Tripartite Gold Commission
THY 	Turkish Airlines
TNC 	Tariff Negotiating Committee (GATT)
TPLF 	Tigrean Peoples Liberation Front
TRSY 	Department of the Treasury
TUAC 	Trade Union Advisory Committee (OECD)
TUC 	Trade Union Conference
TVA 	Tennessee Valley Authority
UANC 	United African National Congress
UAW 	United Auto Workers
UCD 	United Democratic Center
UDEAC 	Central African Customs and Economic Union
UIL 	Italian Labor Union
UMNO 	United Malays National Organization
UMOA 	Union Monetaire Ouest Africaine, West African Monetary
UN 	United Nations
UNAMSIL 	UN Mission in Sierra Leone
UNAUS 	UN Association of the United States of America
UNBRO 	UN Border Relief Operations
UNC 	UN Command in Korea
UNCHC 	UN Committee on Hostages Convention
UNCHS 	UN Commission on Human Settlements
UNCITRAL 	UN Commission on International Trade Law
UNCND 	UN Commission on Narcotic Drugs
UNCRED 	UN Credentials Committee
UNCRIME 	Crime Prevention Control Committee (UN)
UNCSD 	UN Commission on Social Development
UNCSW 	UN Commission on Status of Women
UNCTAD 	UN Conference on Trade and Development
UNDC 	UN Disarmament Commission
UNDOF 	UN Disengagement Observer Force
UNDP 	UN Development Program
UNDRO 	Office of UN Disaster Relief, UN Disaster Relief Coordinator
UNEF 	UN Emergency Force
UNEP 	UN Environment Program
UNESCO 	UN Educational Scientific and Cultural Organization
UNETPSA 	UN Educational and Training Program for Southern Africa
UNFDAC 	UN Fund for Drug Abuse Control
UNFICYP 	UN Force in Cyprus
UNFPA 	UN Fund for Population Activities
UNGA 	UN General Assembly
UNGA/C-1 	Political Committee (UNGA), UN General Assembly First Committee
UNGA/C-2 	UN General Assembly Economic Committee, UN General Assembly Second Committee
UNGA/C-3 	UN General Assembly Social Committee, UN General Assembly Third Committee
UNGA/C-4 	Trusteeship Committee (UNGA), UN General Assembly Fourth Committee
UNGA/C-5 	UN General Assembly Adm and Budget Committee, UN General Assembly Fifth Committee
UNGA/C-6 	UN General Assembly Legal Committee, UN General Assembly Sixth Committee
UNGA/SPC 	UN General Assembly Special Political Committee
UNGOMAP 	UN Good Offices Mission for Afghanistan and Pakistan
UNHCR 	UN High Commissioner for Refugees
UNHRC-1 	UN Human Rights Commission
UNHRC-2 	UN Human Rights Committee
UNICEF 	UN Childrens Fund
UNIDCP 	UN International Drug Control Program
UNIDO 	UN Industrial Development Organization
UNIDROIT 	International Institute for the Unification of Private Law
UNIFIL 	UN Force in Lebanon, UN Interim Force in Lebanon, & UN International Forces in Lebanon
UNIKOM 	UN Iraq-Kuwait Observation Mission
UNITA 	National Union for Total Independence in Angola
UNITAR 	UN Institute for Training and Research
UNMEE 	UN Mission in Ethiopia and Eritrea
UNMIBH 	UN Mission In Bosnia and Herzegovina
UNMIK 	UN Interim Administration Mission in Kosovo
UNMOGIP 	UN Military Observer Group in India and Pakistan
UNMOP 	UN Mission of Observers in Prevlaka
UNO 	United Nicaraguan Opposition
UNOMIG 	UN Observation Mission in Georgia
UNPOP 	UN Population Commission
UNPUOS 	UN Committee on Peaceful Uses of Outer Space
UNRWA 	UN Relief and Works Agency for Palestine Refugees in the Near East
UNSC 	UN Security Council
UNSCEAR 	UN Scientific Committee on the Effects of Atomic Radiation
UNTAT 	UN Transitional Administration in East Timor
UNTC 	Trusteeship Council
UNTER 	Committee on International Terrorism
UNTFSA 	UN Trust Fund for South Africa
UNTNC 	UN Commission on Transnational Corps
UNTSO 	UN Truce Supervision Organization
UPD 	Democratic Popular Unity
UPI 	United Press International
UPOV 	Committee for the Protection for New Varieties of Plants
UPU 	Universal Postal Union
USEGJC 	US-Egypt Joint Cooperation Commission
USEM 	Social Union Mexican Businessmen
USGS 	US Geodetic Survey
USINJC 	US-India Joint Commission on Educational and Cultural Cooperation
USIS 	United States Information Service
USISJC 	US-Israel Joint Committee for Investment and Trade
USNRC 	Nuclear Regulatory Commission
USPS 	US Postal Service
USSAEC 	US-Saudi Arabia Economic Commission
USSS 	US Secret Service
USTR 	Office of the Special Representative for Trade Negotiations
USTTA 	United States Travel and Tourism Administration
VA 	Veterans Administration
VARIG 	S A Empresa De Viacao Area Rio Grandense, Brazilian International Airline
VFW 	Veterans of Foreign Wars
VIASA 	Venezuelan Airline
VOA 	Voice of America
WARC 	World Administrative Radio Conference
WCC 	World Council of Churches
WCL 	International Federation of Christian World Confederation of Labor
WEO 	Western European and Other Groups
WEU 	Western European Union
WFC-2 	World Food Council
WFP 	World Food Program
WFTU 	World Federation of Trade Unions
WHC 	World Heritage Convention (The)
WHO 	World Health Organization
WILPF 	Womens International League for Peace
WIPO 	World Intellectual Property Organization
WJC 	World Jewish Congress
WMO 	World Meteorological Organization
WPO 	Warsaw Pact Organization & Warsaw Treaty Organization
WTO 	World Tourism Organization
WTRO 	World Trade Organization
YPFB 	Yacemientos Petroliferos Fiscales (BL)
ZANU 	Zimbabwe African National Union
ZAPU 	Zimbabwe African Peoples Union
"""


if __name__ == '__main__':
    import codecs
    generate_ctm(codecs.open('./tags.ctm', 'wb', 'utf-8'))
