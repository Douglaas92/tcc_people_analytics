import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def grafico_movimentacao_promovidos(df, indicador, tipo='barras_empilhadas', titulo=''):
    """
    Gera gráficos para analisar a distribuição de promovidos (0 e 1) por grupo.
    """

    if 'promovido' not in df.columns:
        raise ValueError("A coluna 'promovido' precisa estar presente no DataFrame.")

    # Paleta de cores acessível para daltonismo e com bom contraste
    cor_nao_promovido = '#1f77b4'  # Azul
    cor_promovido = '#ff7f0e'      # Laranja

    resumo = df.groupby([indicador, 'promovido'], observed=True).size().unstack(fill_value=0)

    if 0 not in resumo.columns:
        resumo[0] = 0
    if 1 not in resumo.columns:
        resumo[1] = 0

    grupos = resumo.index.astype(str)
    promovido_0 = resumo[0].values
    promovido_1 = resumo[1].values
    total = promovido_0 + promovido_1
    x = np.arange(len(grupos))
    largura = 0.35
    media_geral = None

    fig, ax = plt.subplots(figsize=(16, 9))

    if tipo == 'barras_agrupadas':
        ax.bar(x - largura/2, promovido_0, width=largura, label='Não promovido', color=cor_nao_promovido)
        ax.bar(x + largura/2, promovido_1, width=largura, label='Promovido', color=cor_promovido)

        for i in range(len(x)):
            ax.text(x[i] - largura/2, promovido_0[i] + 15, str(promovido_0[i]), ha='center', fontsize=12)
            ax.text(x[i] + largura/2, promovido_1[i] + 15, str(promovido_1[i]), ha='center', fontsize=12)

        ax.set_title(titulo or f'Distribuição de Promoção por {indicador}', fontsize=18)

    elif tipo == 'barras_empilhadas':
        ax.bar(x, promovido_0, width=largura*2, label='Não promovido', color=cor_nao_promovido)
        ax.bar(x, promovido_1, width=largura*2, bottom=promovido_0, label='Promovido', color=cor_promovido)

        for i in range(len(x)):
            ax.text(x[i], promovido_0[i] / 2, str(promovido_0[i]), ha='center', color='white', fontsize=12)
            ax.text(x[i], promovido_0[i] + promovido_1[i] / 2, str(promovido_1[i]), ha='center', color='white', fontsize=12)

        ax.set_title(titulo or f'Distribuição de Promoção por {indicador}', fontsize=18)

    elif tipo == 'percentual_empilhado':
        pct_0 = promovido_0 / total
        pct_1 = promovido_1 / total

        ax.bar(x, pct_0, width=largura*2, label='Não promovido', color=cor_nao_promovido)
        ax.bar(x, pct_1, width=largura*2, bottom=pct_0, label='Promovido', color=cor_promovido)

        for i in range(len(x)):
            ax.text(x[i], pct_0[i]/2, f'{pct_0[i]*100:.1f}%', ha='center', fontsize=11, color='white')
            ax.text(x[i], pct_0[i] + pct_1[i]/2, f'{pct_1[i]*100:.1f}%', ha='center', fontsize=11, color='white')

        ax.set_ylim(0, 1.1)
        ax.axhline(1, linestyle='--', color='gray')
        ax.set_title(titulo or f'Distribuição de Promoção por {indicador}', fontsize=18)

    elif tipo == 'percentual_agrupado':
        pct_0 = promovido_0 / total
        pct_1 = promovido_1 / total

        ax.bar(x - largura/2, pct_0, width=largura, label='Não promovido', color=cor_nao_promovido)
        ax.bar(x + largura/2, pct_1, width=largura, label='Promovido', color=cor_promovido)

        for i in range(len(x)):
            ax.text(x[i] - largura/2, pct_0[i] + 0.015, f'{pct_0[i]*100:.1f}%', ha='center', fontsize=12)
            ax.text(x[i] + largura/2, pct_1[i] + 0.015, f'{pct_1[i]*100:.1f}%', ha='center', fontsize=12)

        ax.set_ylim(0, 1.1)
        ax.set_title(titulo or f'Distribuição de Promoção por {indicador}', fontsize=18)

    elif tipo == 'taxa_promocao':
        taxa = promovido_1 / total
        taxa = np.nan_to_num(taxa)

        ax.bar(x, taxa, color=cor_promovido, width=largura * 2)
        for i, val in enumerate(taxa):
            ax.text(x[i], val + 0.025, f'{val * 100:.1f}%', ha='center', fontsize=14)

        try:
            media_geral = df['promovido'].astype(float).mean()
            ax.axhline(y=media_geral, linestyle='--', color=cor_nao_promovido, label=f'Média geral: {media_geral * 100:.1f}%')
        except Exception:
            media_geral = None

        ax.set_ylim(0, 1.1)
        ax.set_title(titulo or f'Distribuição de Promoção por {indicador}', fontsize=18)

    elif tipo == 'histograma':
        col = indicador
        data_hist = df.groupby([col, 'promovido'], observed=True).size().unstack(fill_value=0)
        categorias = data_hist.index.astype(str)
        vals_0 = data_hist[0].values
        vals_1 = data_hist[1].values
        x = np.arange(len(categorias))

        ax.bar(x - largura/2, vals_0, width=largura, label='Não promovido', color=cor_nao_promovido)
        ax.bar(x + largura/2, vals_1, width=largura, label='Promovido', color=cor_promovido)

        for i in range(len(x)):
            ax.text(x[i] - largura/2, vals_0[i] + 15, str(vals_0[i]), ha='center', fontsize=12)
            ax.text(x[i] + largura/2, vals_1[i] + 15, str(vals_1[i]), ha='center', fontsize=12)

        ax.set_title(titulo or f'Distribuição de Promoção por {indicador}', fontsize=18)
        grupos = categorias

    else:
        raise ValueError("Tipo inválido.")

    ax.set_xlabel(indicador, fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(grupos, rotation=45, ha='right', fontsize=12)

    if tipo in ['taxa_promocao'] and media_geral is not None:
        ax.legend(title='Legenda', fontsize=12)
    elif tipo != 'taxa_promocao':
        ax.legend(title='Legenda', fontsize=12)

    plt.tight_layout()
    plt.show()

    pass  # substitua pelo conteúdo real
