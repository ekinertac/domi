# -- coding: utf-8 --
import click
import socket

EXTENSIONS = 'com|net|org|abogad|ac|academy|accountant|accountants|actor|ads|adult|africa|ag|agency|airforce|alsace|am|amsterdam|analytics|apartments|app|arab|archi|army|art|asia|associates|at|attorney|auction|audio|author|auto|autos|baby|band|bank|bar|barcelona|bargains|baseball|basketball|bayern|bcn|be|beauty|beer|berlin|best|bet|bible|bid|bike|bingo|bio|biz|black|blackfriday|blog|blue|boats|boo|book|boston|bot|boutique|box|broadway|broker|brussels|budapest|build|builders|business|buy|buzz|bz|bzh|ca|cab|cafe|call|cam|camera|camp|cancerresearch|capetown|capital|car|cards|care|career|careers|cars|casa|cash|casino|catering|catholic|cc|center|ceo|ch|channel|charity|chat|cheap|christmas|church|city|claims|cleaning|click|clinic|clothing|cloud|club|cn|co|co.com|coach|codes|coffee|college|cologne|community|company|computer|comsec|condos|construction|consulting|contact|contractors|cooking|cool|corp|country|coupon|coupons|courses|cpa|credit|creditcard|creditunion|cricket|cruise|cruises|cx|cymru|dad|dance|data|date|dating|day|dds|de|deal|deals|degree|delivery|democrat|dental|dentist|desi|design|dev|diamonds|diet|digital|direct|directory|discount|diy|docs|doctor|dog|domains|dot|download|dubai|dvr|earth|eat|eco|ecom|education|email|energy|engineer|engineering|enterprises|equipment|esq|estate|eu|eus|events|exchange|expert|exposed|express|fail|faith|family|fan|fans|farm|fashion|feedback|film|final|finance|financial|finish|fish|fishing|fit|fitness|flights|florist|flowers|fly|fm|foo|food|football|forsale|forum|foundation|frl|fun|fund|furniture|futbol|fyi|gal|gallery|game|games|garden|gay|ged|gent|gift|gifts|gives|giving|glass|global|gmbh|gold|golf|got|graphics|gratis|green|gripe|grocery|group|gs|guide|guitars|guru|hair|halal|hamburg|haus|health|healthcare|help|helsinki|here|hiphop|hiv|hn|hockey|holdings|holiday|home|homes|horse|hospital|host|hosting|hot|hoteis|hotel|hotels|house|how|idn|im|immo|immobilien|in|inc|industries|info|ing|ink|institute|insurance|insure|international|investments|io|irish|islam|ismaili|ist|istanbul|it|jetzt|jewelry|jobs|joburg|jot|joy|jp|juegos|kaufen|ki|kid|kids|kim|kitchen|kiwi|koeln|kosher|kyoto|la|land|lat|latino|law|lawyer|lc|lease|legal|lgbt|life|lifeinsurance|lifestyle|lighting|like|limited|limo|link|live|living|llc|llp|loan|loans|lol|london|love|ltd|ltda|luxe|luxury|madrid|mail|maison|makeup|management|map|market|marketing|mba|me|med|media|medical|meet|melbourne|meme|memorial|men|menu|miami|mls|mn|mobi|mobile|moda|moe|mom|money|mortgage|moscow|moto|motorcycles|mov|movie|music|mutualfunds|mx|nagoya|name|navy|network|new|news|nf|ngo|ninja|nl|now|nrw|nyc|okinawa|one|ong|onl|online|ooo|organic|osaka|ott|paris|pars|partners|parts|party|pay|pet|pets|phd|phone|photo|photography|photos|physio|pics|pictures|pid|ping|pink|pizza|place|play|plumbing|plus|pm|poker|politie|porn|press|pro|productions|prof|promo|properties|property|protection|pub|pw|qpon|quebec|racing|radio|read|realestate|realtor|realty|recipes|red|rehab|reise|reisen|rent|rentals|repair|report|republican|rest|restaurant|retirement|review|reviews|rich|rip|rocks|rodeo|roma|room|rsvp|rugby|ruhr|run|ryukyu|saarland|safe|safety|sale|salon|sari|sarl|save|sb|sc|scholarships|school|schule|science|scot|se|search|secure|security|services|sex|sexy|sh|shabaka|shabaka-arabic|shia|shiksha|shoes|shop|shopping|show|singles|site|ski|smile|soccer|social|software|solar|solutions|song|soy|spa|space|sport|sports|spot|srl|stockholm|storage|store|stream|studio|study|style|sucks|supplies|supply|support|surf|surgery|swiss|sydney|systems|taipei|talk|tatar|tattoo|tax|taxi|team|tech|technology|tel|tennis|thai|theater|theatre|tickets|tienda|tips|tires|tirol|tl|today|tokyo|tools|top|tours|town|toys|trade|trading|training|travel|tube|tv|tw|uk|university|uno|us|us.com|vacations|vc|vegas|ventures|versicherung|vet|viajes|video|villas|vin|vip|vision|vlaanderen|vodka|vote|voting|voto|voyage|wales|wang|watch|watches|weather|web|webcam|webs|website|wedding|wf|wiki|win|wine|winners|work|works|world|wow|ws|wtf|xxx|xyz|yachts|yoga|yokohama|you|zero|zip|zone|netvc|cm|comsg|jpnet|hunet|fr|orgvc|eucom|orgpe|cocom|couk|es|combz|netbz|alert|mexcom|comde|cobz|li|senet|innet|pe|rucom|comse|brcom|sacom|compe|jpncom|cncom|comvc|meuk|grcom|gbnet|ukcom|nomes|orguk|usorg|comau|uscom|zacom|uknet|nu|aeorg|netau|decom|netpe|krd|orges|sg|orgau|comes'


def check_availability(query, extension, **options):
    domain = "%s.%s" % (query, extension) if extension else query

    try:
        socket.gethostbyname(domain)
        return False
    except:
        return True


def search(query, **options):
    result = ""
    available_extensions = sorted(EXTENSIONS.split('|'))

    # Loop only TLDs
    if options['tld']:
        available_extensions = "com|net|org".split('|')

    # Pass raw query to availability check
    if options['no_suggest']:
        status = check_availability(query, False)
        # Clean available extensions
        available_extensions = []
        message = "Available" if status else "Not Available"
        color = 'green' if status else 'red'
        click.echo(click.style(message, fg=color))


    for ext in available_extensions:
        status = check_availability(query, ext, **options)

        # Print only available and pass the unavailable domains
        if options['available'] and not status:
            continue

        # Async options
        new_line = "\n" if options['sync'] else "\r"

        # Color options
        color = "green" if status else "red"
        ascii_status = "+" if status else "x"

        # Color output
        ascii_output = "%s %s.%s%s" % (ascii_status, query, ext, new_line)
        color_output = "%s.%s%s" % (query, click.style(ext, fg=color), new_line)
        output = ascii_output if options['no_color'] else color_output

        # Async Output
        if not options['sync']:
            print output
        else:
            result += output

    if options['sync']:
        click.echo_via_pager(result)



@click.command()
@click.version_option()
@click.option(
    '--no-color',
    '-c',
    is_flag=True,
    help="Disable colorful output"
)
@click.option(
    '--available',
    '-a',
    is_flag=True,
    help="Show only available domains"
)
@click.option(
    '--no-suggest',
    '-n',
    is_flag=True,
    help="Search exact domain query."
)
@click.option(
    '--tld',
    '-t',
    is_flag=True,
    help="Show only top level domains. (.com, .net, .org)"
)
@click.option(
    '--sync',
    '-s',
    is_flag=True,
    help="Print domain names (with pager) once when query complete for each domain"
)
@click.argument('query')
def cli(no_color, available, no_suggest, tld, sync, query):
    "Domi - Terminal based quick domain search tool."
    options = {
        "no_color": no_color,
        "available": available,
        "no_suggest": no_suggest,
        "tld": tld,
        "sync": sync
    }
    click.echo(search(query, **options))


