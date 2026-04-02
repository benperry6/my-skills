# my-personal-paid-tracking-foundation

`my-personal-paid-tracking-foundation` est un skill personnel de doctrine.

Il existe pour eviter de refaire, projet par projet, la meme discussion sur la bonne fondation de tracking paid media quand on veut rester serieux techniquement sans depenser trop tot une infra enterprise.

## Ce que ce skill fait

Ce skill prend un nouveau projet ou un projet existant et tranche la bonne fondation de tracking paid media selon :

- le type de projet
- le stade de maturite
- le budget reel
- les canaux payants prevus
- la stack deja en place

Il ne se contente pas d'expliquer.

Il doit :

- diagnostiquer le contexte
- recommander une stack claire
- expliquer pourquoi
- produire un plan d'implementation concret
- lister ce que l'agent peut faire et ce que l'utilisateur doit fournir

## Architecture canonique en 4 etapes

Ce skill doit raisonner explicitement en 4 grandes etapes :

### 1. Preparer la codebase

Implementer la fondation tracking dans le site ou l'app :

- choisir la bonne stack
- definir le bon modele d'evenements
- adapter la codebase pour que les plateformes puissent etre branchees ensuite

### 2. Bootstrapper les acces vendor

Donner au skill les acces machine-to-machine dont il a besoin pour les plateformes approuvees :

- reutiliser ou recreer les acces Google / Meta / autres
- verifier les vraies permissions, scopes, tokens, projets et businesses
- stocker proprement l'etat d'acces reutilisable

### 3. Brancher et administrer les plateformes

Utiliser ces acces pour operer la couche paid media reelle :

- creer les assets vendors
- relier les services entre eux quand le chemin API est reel et verifie
- connecter concretement la codebase aux plateformes

### 4. Verifier le flux de donnees en comportement reel

Prouver que l'implementation envoie vraiment les donnees utiles :

- verifier le chargement runtime des vendors apres consentement quand c'est pertinent
- verifier les relais server-side / first-party quand ils existent
- verifier l'ingestion finale vendor avec la meilleure voie disponible, idealement en CLI/API
- documenter le runbook de verification et de debug pour pouvoir le reutiliser sur les projets suivants

### Garde-fous de passage

- finir l'etape 2 ne veut **pas** dire que l'etape 3 est finie
- finir l'etape 3 ne veut **pas** dire que l'etape 4 est finie
- avoir Google comme cluster par defaut ne veut **pas** dire que toutes les liaisons Google sont deja prouvees
- creer un asset ou une liaison ne veut **pas** dire que les donnees remontent deja en comportement reel
- une etape n'est consideree complete que si son resultat est verifie en comportement reel, pas seulement documente

## La these derriere ce skill

Le probleme recurrent n'est pas de savoir si le tracking paid media est utile. Il l'est.

Le vrai probleme est de savoir **quoi installer maintenant**, **quoi repousser**, et **quand monter en gamme** sans:

- sur-investir avant d'avoir du revenu
- perdre des donnees utiles trop longtemps
- bricoler une stack incoherente qu'il faudra jeter plus tard

La doctrine capturee ici est simple :

- en phase pre-revenus, on veut deja collecter proprement
- mais on ne paie pas une infra lourde juste "au cas ou"
- le browser-side seul est insuffisant
- le server-side pur n'est pas la bonne reponse non plus
- la bonne fondation de depart est en general **hybride**
- Google et Meta sont les bases par defaut; dans le cluster Google, la base par defaut est `GTM web + GA4 + GSC + Google Ads`, puis toute autre regie peut etre ouverte des le depart seulement si elle est reellement coherente avec le produit et le channel plan
- pour un site possede en propre, la base search doit aussi inclure `Bing Webmaster Tools`, avec une verification canonique du domaine via le provider DNS autoritatif quand on veut couvrir tout le domaine; le registrar et le DNS host peuvent etre differents, et dans le setup reel verifie ici `lostnfound-app.com` est en `Hostinger registrar + Cloudflare DNS`; dans le flow Bing reel verifie ici, la methode etait un `CNAME`, pas un `TXT`, et le site reste modele comme une URL (`https://lostnfound-app.com/`) plutot que comme une propriete de type `sc-domain:`
- les vendors nommes dans le skill sont des exemples, pas une whitelist; le skill peut recommander une regie non nommee si elle est vraiment pertinente pour le contexte business
- avant toute action en navigateur sur une regie ou plateforme tierce, on verifie explicitement si un chemin CLI/API/MCP existe
- quand ce chemin programmatique existe, on le sonde en vrai avec un read/write probe adapte pour verifier qu'il fonctionne depuis la machine et les credentials courants
- si ce chemin programmatique existe et fonctionne, il devient la voie obligatoire par defaut; le navigateur n'est autorise que s'il est absent, casse, ou insuffisant pour l'operation exacte
- le navigateur reste donc un fallback de bootstrap justifie, pas le mode operatoire par defaut
- si l'utilisateur demande un navigateur particulier pour une tache, un compte ou un flow precis, cette instruction est limitee a ce scope; elle ne devient pas une preference implicite pour le reste de la session, et hors de ce scope on revient a la regle globale par defaut
- quand un onglet navigateur existant est reutilise comme source d'etat vendor, on le recharge avant d'en tirer une conclusion; seule exception: un onglet ouvert par l'investigation en cours, juste avant la lecture, n'a pas besoin d'un refresh supplementaire
- pour Google Ads et les structures similaires a plusieurs comptes, on nomme le compte manager comme une couche parapluie/admin et non comme un projet, puis on donne a chaque business son propre compte client dedie nomme avec le nom du business; quand ce compte client dedie existe, la propriete GA4 du business doit etre liee directement a ce compte client et non au MCC par defaut; un compte legacy qui ne peut pas etre retire doit etre marque explicitement comme legacy pour eviter toute confusion
- si Google impose un fallback navigateur, la seule preuve d'identite valable est l'adresse email visible du compte actif dans le switcher en haut a droite; `authuser=*`, `login_hint` et les index de compte ne sont pas des preuves fiables, et il faut preferer ouvrir les formulaires/supports Google depuis une session vendor deja verifiee sur le bon compte
- pour toute regie, on vise les permissions machine-to-machine les plus larges et pertinentes que le flow officiel expose reellement, puis on verifie en vrai les scopes et capacites accordes
- quand le flow officiel expose dynamiquement la liste des permissions ou la duree du token, on inspecte les options reelles au moment du bootstrap au lieu de figer une liste historique dans le skill
- quand une regie permet un token machine-to-machine non expirant, on le prefere et on verifie ensuite l'etat d'expiration reel du token
- on ne choisit jamais un compte, business ou projet cloud sans validation explicite de l'utilisateur si plusieurs options existent
- on reutilise d'abord les acces deja disponibles sur la machine quand ils correspondent au bon business et sont approuves
- quand une regie n'etait pas encore documentee, ou quand un flow documente est devenu obsolete, on ne met a jour le skill qu'apres avoir reussi a reproduire un chemin qui fonctionne en comportement reel
- le skill doit donc apprendre en continu, mais uniquement a partir de learnings verifies en pratique, jamais a partir de theorie seule ou de docs non testees
- les fichiers d'auth qui doivent absolument rester sur disque pour des outils officiels peuvent rester dans leurs emplacements standards, mais avec des permissions strictes
- les secrets et blobs de bootstrap rematerialisables doivent aller dans un secret store local securise; si `1Password CLI` est reellement disponible et voulu, il peut devenir le backend privilegie, sinon le Keychain macOS est le fallback par defaut
- quand un nom canonique est utile pour les objets vendors, il doit decrire le mecanisme d'acces cree; la convention preferee est `Paid Media Vendor M2M API Access`, avec une variante courte seulement si une plateforme impose une limite de longueur

## Ce que ce skill couvre

- le choix de fondation paid tracking budget-friendly
- la priorisation des vendors a ouvrir
- le bon niveau d'ambition selon le type de projet
- les pre-requis d'acces et d'identifiants
- la facon d'obtenir ces acces et identifiants par voie programmatique quand c'est possible
- la facon de verifier ensuite les flux de donnees en comportement reel et de documenter les runbooks de debug reutilisables
- la facon d'obtenir le jeu de permissions et la duree de token les plus larges que le flow officiel expose reellement au moment du bootstrap
- la selection explicite du bon compte / business / projet avant toute action
- la capitalisation des nouveaux learnings verifies quand on documente une nouvelle regie ou qu'on corrige une procedure devenue obsolete
- le moment ou il faut passer d'une fondation low-cost a une infra plus robuste

## Ce que ce skill ne couvre pas

- la strategie de campagnes paid media elle-meme
- la creation des creatives
- le tracking produit generaliste hors paid media
- le parametrage detaille d'une plateforme specifique quand il faut des procedures tres locales
- les bootstraps vendors impossibles sans permissions, tokens ou autorisations OAuth/developer
- les secrets live dans le repo du skill

## Comment il s'articule avec d'autres skills

- Utiliser ce skill **d'abord** quand la question est "quelle fondation tracking faut-il installer ?"
- Utiliser ensuite `analytics-tracking` pour approfondir l'implementation de mesure si besoin.
- Utiliser `paid-ads` pour la strategie de campagnes, le ciblage et l'optimisation media.

## Principe d'usage

Ce skill doit rester opinionated.

Sa valeur n'est pas de lister toutes les options possibles.
Sa valeur est de recommander la bonne base par defaut, en expliquant les trade-offs et en donnant un plan directement executable, y compris le chemin programmatique d'obtention des acces quand ce chemin existe.
