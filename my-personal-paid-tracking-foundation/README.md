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
- Google et Meta sont les bases par defaut, puis toute autre regie peut etre ouverte des le depart seulement si elle est reellement coherente avec le produit et le channel plan
- avant de suggerer le navigateur, on recherche sur internet dans les docs officielles et les APIs si un chemin machine-to-machine credible existe
- quand une regie expose un vrai chemin machine-to-machine credible, on privilegie API/CLI/MCP avant le navigateur
- le navigateur reste un fallback de bootstrap, pas le mode operatoire par defaut
- pour toute regie, on vise les permissions machine-to-machine les plus larges et pertinentes que le flow officiel expose reellement, puis on verifie en vrai les scopes et capacites accordes
- on ne choisit jamais un compte, business ou projet cloud sans validation explicite de l'utilisateur si plusieurs options existent
- on reutilise d'abord les acces deja disponibles sur la machine quand ils correspondent au bon business et sont approuves
- les fichiers d'auth qui doivent absolument rester sur disque pour des outils officiels peuvent rester dans leurs emplacements standards, mais avec des permissions strictes
- les secrets et blobs de bootstrap rematerialisables doivent aller dans un secret store local securise; si `1Password CLI` est reellement disponible et voulu, il peut devenir le backend privilegie, sinon le Keychain macOS est le fallback par defaut

## Ce que ce skill couvre

- le choix de fondation paid tracking budget-friendly
- la priorisation des vendors a ouvrir
- le bon niveau d'ambition selon le type de projet
- les pre-requis d'acces et d'identifiants
- la facon d'obtenir ces acces et identifiants par voie programmatique quand c'est possible
- la selection explicite du bon compte / business / projet avant toute action
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
