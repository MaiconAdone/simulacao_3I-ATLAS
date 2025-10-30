# simulacao_3I-ATLAS
# Simulação da Passagem do 3I/ATLAS (C/2025 N1) pelo Sistema Solar

Este projeto executa uma **simulação preditiva simplificada (2-corpos)** da trajetória do objeto **interestelar 3I/ATLAS (C/2025 N1)** — um cometa/asteroide detectado em 2025 com órbita **hiperbólica**, que passará próximo ao nosso Sistema Solar no **final de outubro de 2025**.

A simulação calcula e exibe:

- 📈 **Gráfico da distância heliocêntrica** ao longo do tempo (±200 dias do periélio)  
- 🌀 **Trajetória no plano perifocal**, mostrando o Sol e as órbitas aproximadas de 1 UA e de Marte  

Os resultados são salvos como imagens PNG no diretório de execução.

---

## Conceito Físico

O modelo é baseado nas **equações hiperbólicas de Kepler** para um sistema de dois corpos (Sol e 3I/ATLAS), ignorando perturbações planetárias e acelerações não gravitacionais.  
Apesar de simples, ele fornece uma **estimativa precisa do tempo de periélio e do comportamento orbital** ao redor do Sol.

### Parâmetros orbitais usados
| Parâmetro | Valor | Descrição |
|------------|--------|-----------|
| `q` | 1.3565 UA | Distância de periélio |
| `a` | -0.26549 UA | Semi-eixo maior (hiperbólico) |
| `e` | ≈ 6.11 | Excentricidade |
| `T_peri` | 29/10/2025 11:15 UTC | Época de periélio aproximada |

---

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seuusuario/simulacao-3I-ATLAS.git
cd simulacao-3I-ATLAS
pip install -r requirements.txt
```
## Licença

Este projeto está sob a licença MIT — livre para uso e modificação.

## Autor

Maicon Adone //
LinkedIn: https://www.linkedin.com/in/maiconadone/
GitHub: https://github.com/MaiconAdone
