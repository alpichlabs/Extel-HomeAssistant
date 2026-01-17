🚪 Extel Umii pour Home Assistant
Cette intégration personnalisée permet de contrôler les portails motorisés de la gamme Extel et Avidsen utilisant l'application Umii directement depuis Home Assistant.
✨ Caractéristiques
• Contrôle Complet : Ouverture, Fermeture et Arrêt (Stop).
• Ouverture Piéton : Un bouton dédié pour l'ouverture partielle (HALF-OPEN).
• Retour d'État : Suivi en temps réel de l'état du portail (Ouvert/Fermé).
• Sécurité : Génération d'un identifiant d'appareil unique pour éviter les conflits avec l'application mobile officielle.
• Multi-Appareils : Détection automatique de tous les portails liés à votre compte Umii.

🚀 Installation
Méthode 1 : HACS (Recommandé)
1. Assurez-vous que HACS est installé.
2. Allez dans HACS > Intégrations.
3. Cliquez sur les 3 points en haut à droite et choisissez Dépôts personnalisés.
4. Collez l'URL de ce dépôt : https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_DEPOT.
5. Sélectionnez la catégorie Intégration et cliquez sur Ajouter.
6. Cherchez Extel Umii dans la liste et cliquez sur Télécharger.
7. Redémarrez Home Assistant.
Méthode 2 : Manuelle
1. Téléchargez le dossier custom_components/extel_umii.
2. Copiez-le dans le dossier custom_components de votre installation Home Assistant.
3. Redémarrez Home Assistant.
⚙️ Configuration
1. Allez dans Paramètres > Appareils et services.
2. Cliquez sur Ajouter une intégration en bas à droite.
3. Recherchez Extel Portail.
4. Entrez vos identifiants Umii (Email et Mot de passe).
5. Sélectionnez votre portail dans la liste proposée.
## 🛠️ Entités créées

| Nom de l'entité | Type | Description |
| :--- | :--- | :--- |
| `cover.portail_jardin` | **Cover** | Contrôle principal : Ouverture, Fermeture et Arrêt (Stop). |
| `button.ouverture_pieton` | **Button** | Déclenche l'ouverture partielle (HALF-OPEN) du portail. |

⚠️ Avertissement
Cette intégration est un projet communautaire non-officiel. Elle n'est ni affiliée, ni approuvée par Extel ou Avidsen. L'utilisation de cette intégration se fait à vos propres risques.
🤝 Contribution
Les contributions sont les bienvenues ! Si vous avez une idée d'amélioration ou si vous trouvez un bug, n'hésitez pas à ouvrir une Issue ou une Pull Request.
📄 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
