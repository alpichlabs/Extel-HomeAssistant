# 🚪 Extel Umii pour Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Cette intégration personnalisée permet de piloter les portails motorisés des marques **Extel** et **Avidsen** utilisant l'application **Umii** directement depuis Home Assistant.

---

## ✨ Caractéristiques

* **Contrôle Complet** : Ouverture, Fermeture et Arrêt (Stop).
* **Ouverture Piéton** : Un bouton dédié pour l'ouverture partielle (`HALF-OPEN`).
* **Retour d'État** : Suivi en temps réel de l'état du portail (Ouvert/Fermé).
* **Sécurité** : Génération d'un identifiant d'appareil unique (UUID) pour éviter tout conflit avec votre application mobile.
* **Multi-Appareils** : Détection et installation automatique de tous les portails liés à votre compte.

---

## 🚀 Installation

### Méthode 1 : HACS (Recommandé)

1.  Assurez-vous que [HACS](https://hacs.xyz/) est installé.
2.  Allez dans **HACS** > **Intégrations**.
3.  Cliquez sur les **3 points** en haut à droite et choisissez **Dépôts personnalisés**.
4.  Collez l'URL de ce dépôt : `https://github.com/jasonpretavoine/Extel-HomeAssistant`.
5.  Sélectionnez la catégorie **Intégration** et cliquez sur **Ajouter**.
6.  Cherchez **Extel Umii** dans la liste et cliquez sur **Télécharger**.
7.  **Redémarrez Home Assistant**.

### Méthode 2 : Manuelle

1.  Téléchargez le dossier `custom_components/extel_umii`.
2.  Copiez-le dans le dossier `custom_components` de votre installation Home Assistant.
3.  **Redémarrez Home Assistant**.

---

## ⚙️ Configuration

1.  Allez dans **Paramètres** > **Appareils et services**.
2.  Cliquez sur **Ajouter une intégration** en bas à droite.
3.  Recherchez **Extel Portail**.
4.  Entrez vos identifiants Umii (Email et Mot de passe).
5.  Sélectionnez votre portail dans la liste proposée.

---

## 🛠️ Entités créées

| Nom de l'entité | Type | Description |
| :--- | :--- | :--- |
| `cover.portail_jardin` | **Cover** | Contrôle principal : Ouverture, Fermeture et Arrêt (Stop). |
| `button.ouverture_pieton` | **Button** | Déclenche l'ouverture partielle (HALF-OPEN) du portail. |

---

## ⚠️ Avertissement

Cette intégration est un projet communautaire **non-officiel**. Elle n'est ni affiliée, ni approuvée par **Extel** ou **Avidsen**. L'utilisation de cette intégration se fait à vos propres risques et périls.

---

## 🤝 Contribution

Si vous souhaitez améliorer cette intégration ou signaler un bug :
1.  Ouvrez une **Issue** pour signaler un problème.
2.  Soumettez une **Pull Request** pour proposer des changements.

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
