# Preference learning

## Remarque

Les zones limites d'indifférence et d'incomparabilité sont fixées par les valeurs de gamma_ij et gamma_ji et dépendent de Pf.

f_I = max(gamma_ij, gamma_ji) + |gamma_ij - gamma_ji|/Pf
f_J = min(gamma_ij, gamma_ji) - |gamma_ij - gamma_ji|/Pf

=> La réponse donnée par l'utilisateur donne la zone dans laquelle on se situe (quel intervalle pour I et J)

### Exemple pour une paire
[gamma_ij, gamma_ji] = [0.5 ; 0.4]

incomparabilité     ->  J < [0.3 ; 0.399],  I <= J
indifférence        ->  I > [0.501 ; 0.6],  J >= I
préférence          ->  J > [0.3 ; 0.399],  I < [0.501 ; 0.6],  I <= J





### Exemple : si l'utilisateur se prononce pour 
l'incomparabilité pour une paire dont f_J ~= 0.3
l'indifférence pour une paire dont f_I ~= 0.2

on sait que I et J appartiennent à l'intervalle [0.2, 0.3] car I <= J et I > 0.2, J < 0.3



## Choix des valeurs des paramètres

Pour choisir I et J -> on minimise la valeur de J et on maximise celle de I     si pas de conflit
                    -> on choisit les valeurs minimisant le conflit             si conflit


Pour choisir Pf -> on minimise la valeur de Pf                                  si pas de conflit
                -> on choisit la valeur minimisant le conflit                   si conflit


conflit -> contradiction entre deux choix de l'utilisateur


## Algorithme

1. on propose n paires choisies aléatoirement à l'utilisateur

2. On calcule les zones limites pour chaque paire
    - f_I = (x, y) où x = max(gamma_ij, gamma_ji) et y = |gamma_ij - gamma_ji| (frontière exacte = x + y/Pf)
    - f_J = (x, y) où x = min(gamma_ij, gamma_ji) et y = |gamma_ij - gamma_ji| (frontière exacte = x - y/Pf)

3. Grâce au choix de l'utilisateur et à ces tuples, on calcule pour chaque paire (I_max, J_min, Pf_min, Pf_max)

4. On compare les paires
    - Abscence de conflit : on prend le plus petit I_max et le plus grand J_min comme valeurs de I et J ainsi que le plus grand Pf_min comme valeur de Pf
    - Conflit : optimisation pour minimiser le conflit