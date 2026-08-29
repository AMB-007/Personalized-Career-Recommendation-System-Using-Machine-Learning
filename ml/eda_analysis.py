"""
Exploratory Data Analysis (EDA) Module for Career Recommendation System.
Generates comprehensive statistical profiles and high-resolution visualizations.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Set style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Datasets"
OUTPUT_DIR = BASE_DIR / "ml" / "reports" / "eda_figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_datasets():
    """Loads raw compatibility and career requirement datasets."""
    compat_path = DATA_DIR / "Student_Career_Compatibility_V2_RAW.csv"
    req_path = DATA_DIR / "Career_Knowledge_Requirements_V2_RAW.csv"

    print(f"Loading datasets from {DATA_DIR}...")
    compat_df = pd.read_csv(compat_path)
    req_df = pd.read_csv(req_path)
    print(f"Loaded Compatibility Data: {compat_df.shape[0]:,} rows, {compat_df.shape[1]} columns")
    print(f"Loaded Career Requirements: {req_df.shape[0]:,} rows, {req_df.shape[1]} columns")
    return compat_df, req_df


def plot_target_and_score_distribution(df: pd.DataFrame):
    """Figure 1: Target Label Class Balance & Compatibility Score Distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # 1. Target Class Balance
    counts = df['compatibility_label'].value_counts()
    percentages = df['compatibility_label'].value_counts(normalize=True) * 100
    labels = ['Compatible (1)', 'Incompatible (0)']
    colors = ['#10b981', '#f43f5e']

    bars = axes[0].bar(labels, [counts[1], counts[0]], color=colors, width=0.5, edgecolor='#0f172a', alpha=0.9)
    axes[0].set_title('Target Class Distribution (compatibility_label)', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_ylabel('Record Count', fontsize=11)
    axes[0].set_ylim(0, max(counts) * 1.18)

    for bar, count, pct in zip(bars, [counts[1], counts[0]], [percentages[1], percentages[0]]):
        height = bar.get_height()
        axes[0].text(
            bar.get_x() + bar.get_width() / 2.,
            height + 4000,
            f'{count:,}\n({pct:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1e293b'
        )

    # 2. Compatibility Score Distribution by Class
    sns.kdeplot(
        data=df[df['compatibility_label'] == 1],
        x='compatibility_score',
        ax=axes[1],
        fill=True,
        color='#10b981',
        label='Compatible (1)',
        alpha=0.4,
        linewidth=2
    )
    sns.kdeplot(
        data=df[df['compatibility_label'] == 0],
        x='compatibility_score',
        ax=axes[1],
        fill=True,
        color='#f43f5e',
        label='Incompatible (0)',
        alpha=0.4,
        linewidth=2
    )
    axes[1].axvline(df['compatibility_score'].mean(), color='#3b82f6', linestyle='--', linewidth=1.8,
                    label=f"Mean ({df['compatibility_score'].mean():.1f})")
    axes[1].set_title('Compatibility Score Density by Target Class', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Compatibility Score (%)', fontsize=11)
    axes[1].set_ylabel('Density', fontsize=11)
    axes[1].legend(frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "01_target_distribution.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_demographic_analysis(df: pd.DataFrame):
    """Figure 2: Demographic Patterns (Age, Class, Academic Stream vs Compatibility)."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)

    # 1. Compatibility Rate by Age
    age_stats = df.groupby('age')['compatibility_label'].agg(['count', 'mean']).reset_index()
    sns.barplot(data=age_stats, x='age', y='mean', hue='age', ax=axes[0], palette='Blues_r', edgecolor='#1e293b', legend=False)
    axes[0].set_title('Compatibility Rate by Student Age', fontsize=12, fontweight='bold', pad=10)
    axes[0].set_xlabel('Age (Years)', fontsize=11)
    axes[0].set_ylabel('Compatibility Rate (Proportion)', fontsize=11)
    axes[0].set_ylim(0, 1.0)
    for p in axes[0].patches:
        axes[0].annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

    # 2. Compatibility Rate by School Class
    class_stats = df.groupby('class')['compatibility_label'].agg(['count', 'mean']).reset_index()
    sns.barplot(data=class_stats, x='class', y='mean', hue='class', ax=axes[1], palette='Purples_r', edgecolor='#1e293b', legend=False)
    axes[1].set_title('Compatibility Rate by School Class', fontsize=12, fontweight='bold', pad=10)
    axes[1].set_xlabel('Class / Grade Level', fontsize=11)
    axes[1].set_ylabel('Compatibility Rate (Proportion)', fontsize=11)
    axes[1].set_ylim(0, 1.0)
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

    # 3. Compatibility Rate & Volume by Stream
    stream_stats = df.groupby('stream')['compatibility_label'].agg(['count', 'mean']).reset_index()
    sns.barplot(data=stream_stats, x='stream', y='mean', hue='stream', ax=axes[2], palette='mako', edgecolor='#1e293b', legend=False)
    axes[2].set_title('Compatibility Rate by Academic Stream', fontsize=12, fontweight='bold', pad=10)
    axes[2].set_xlabel('Stream', fontsize=11)
    axes[2].set_ylabel('Compatibility Rate (Proportion)', fontsize=11)
    axes[2].set_ylim(0, 1.0)
    axes[2].tick_params(axis='x', rotation=20)
    for p in axes[2].patches:
        axes[2].annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

    plt.tight_layout()
    out_file = OUTPUT_DIR / "02_demographic_distributions.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_match_components(df: pd.DataFrame):
    """Figure 3: Four Core Match Components Distribution (Ability, Interest, Academic, Learning)."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), dpi=300)
    components = [
        ('ability_match_component', 'Ability Match Component (8D Aptitude Alignment)', '#3b82f6', (0, 0)),
        ('interest_match_component', 'Interest Match Component (10D Disciplinary Alignment)', '#10b981', (0, 1)),
        ('academic_match_component', 'Academic Match Component (Grade / Percentage)', '#f59e0b', (1, 0)),
        ('learning_match_component', 'Learning Match Component (Agility Score)', '#8b5cf6', (1, 1)),
    ]

    for col, title, color, (r, c) in components:
        ax = axes[r, c]
        sns.kdeplot(
            data=df[df['compatibility_label'] == 1],
            x=col,
            ax=ax,
            fill=True,
            color='#10b981',
            label='Compatible (1)',
            alpha=0.35,
            linewidth=2
        )
        sns.kdeplot(
            data=df[df['compatibility_label'] == 0],
            x=col,
            ax=ax,
            fill=True,
            color='#f43f5e',
            label='Incompatible (0)',
            alpha=0.35,
            linewidth=2
        )
        mean_val = df[col].mean()
        ax.axvline(mean_val, color=color, linestyle='--', linewidth=1.5, label=f'Mean ({mean_val:.1f})')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel('Component Score (0-100)', fontsize=10)
        ax.set_ylabel('Density', fontsize=10)
        ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.85)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "03_match_components_kde.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_correlation_heatmap(df: pd.DataFrame):
    """Figure 4: Correlation Matrix Heatmap across Numerical Variables."""
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    num_cols = [
        'age', 'class', 'ability_match_component', 'interest_match_component',
        'academic_match_component', 'learning_match_component',
        'compatibility_score', 'compatibility_label'
    ]
    corr = df[num_cols].corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(
        corr,
        mask=mask,
        cmap=cmap,
        vmax=1.0,
        vmin=-0.5,
        center=0,
        square=True,
        linewidths=0.8,
        cbar_kws={"shrink": .8},
        annot=True,
        fmt='.2f',
        annot_kws={'size': 10, 'weight': 'bold'},
        ax=ax
    )
    ax.set_title('Correlation Matrix of ML Features and Targets', fontsize=14, fontweight='bold', pad=15)
    plt.xticks(rotation=35, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "04_correlation_matrix.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_career_domains_and_clusters(df: pd.DataFrame):
    """Figure 5: Career Domains and Cluster Volume & Compatibility Distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

    # 1. Top Career Domains by Sample Volume
    dom_stats = df.groupby('career_domain').agg(
        total_evaluations=('compatibility_label', 'count'),
        compat_rate=('compatibility_label', 'mean')
    ).sort_values('total_evaluations', ascending=True).tail(12)

    y_pos = np.arange(len(dom_stats))
    bars = axes[0].barh(y_pos, dom_stats['total_evaluations'], color='#38bdf8', edgecolor='#0f172a', alpha=0.85)
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(dom_stats.index, fontsize=10)
    axes[0].set_title('Top 12 Career Domains by Candidate Volume', fontsize=12, fontweight='bold', pad=10)
    axes[0].set_xlabel('Total Pairwise Evaluations', fontsize=10)

    for bar in bars:
        w = bar.get_width()
        axes[0].text(w + 200, bar.get_y() + bar.get_height()/2, f"{int(w):,}",
                     va='center', ha='left', fontsize=9, color='#1e293b', fontweight='semibold')

    # 2. Compatibility Rate across Top Domains
    dom_sorted_rate = dom_stats.sort_values('compat_rate', ascending=True)
    bars2 = axes[1].barh(
        np.arange(len(dom_sorted_rate)),
        dom_sorted_rate['compat_rate'] * 100,
        color='#818cf8',
        edgecolor='#0f172a',
        alpha=0.85
    )
    axes[1].set_yticks(np.arange(len(dom_sorted_rate)))
    axes[1].set_yticklabels(dom_sorted_rate.index, fontsize=10)
    axes[1].set_title('Compatibility Success Rate by Career Domain (%)', fontsize=12, fontweight='bold', pad=10)
    axes[1].set_xlabel('Compatible Pairs (%)', fontsize=10)
    axes[1].set_xlim(0, 100)

    for bar in bars2:
        w = bar.get_width()
        axes[1].text(w + 1.0, bar.get_y() + bar.get_height()/2, f"{w:.1f}%",
                     va='center', ha='left', fontsize=9, color='#1e293b', fontweight='semibold')

    plt.tight_layout()
    out_file = OUTPUT_DIR / "05_career_domain_distribution.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_multivariate_interactions(df: pd.DataFrame):
    """Figure 6: Bivariate Ability Match vs Interest Match Interaction."""
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)

    # Sample points for clean scatter rendering
    sample_df = df.sample(n=min(12000, len(df)), random_state=42)

    scatter = ax.scatter(
        sample_df['ability_match_component'],
        sample_df['interest_match_component'],
        c=sample_df['compatibility_label'],
        cmap=matplotlib.colors.ListedColormap(['#f43f5e', '#10b981']),
        alpha=0.45,
        s=16,
        edgecolors='none'
    )

    ax.set_title('Bivariate Interaction: Ability Match vs. Interest Match by Compatibility', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Ability Match Component (0-100)', fontsize=11)
    ax.set_ylabel('Interest Match Component (0-100)', fontsize=11)

    cbar = plt.colorbar(scatter, ax=ax, ticks=[0.25, 0.75])
    cbar.ax.set_yticklabels(['Incompatible (0)', 'Compatible (1)'], fontsize=10, fontweight='bold')
    cbar.set_label('Classification Target', fontsize=11)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "06_multivariate_pairplot.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def generate_eda_summary_dashboard(df: pd.DataFrame):
    """Figure 7: Unified 6-Panel Executive EDA Dashboard."""
    fig = plt.figure(figsize=(18, 12), dpi=300)
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.25)

    # 1. Target Pie
    ax1 = fig.add_subplot(gs[0, 0])
    counts = df['compatibility_label'].value_counts()
    ax1.pie(
        [counts[1], counts[0]],
        labels=['Compatible (72.2%)', 'Incompatible (27.8%)'],
        colors=['#10b981', '#f43f5e'],
        autopct='%1.1f%%',
        startangle=140,
        wedgeprops=dict(width=0.45, edgecolor='#0f172a')
    )
    ax1.set_title('1. Target Class Split', fontsize=12, fontweight='bold')

    # 2. Score Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    sns.histplot(df['compatibility_score'], kde=True, ax=ax2, color='#6366f1', bins=40)
    ax2.set_title('2. Overall Compatibility Score Distribution', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Score (%)', fontsize=10)

    # 3. Stream Comparison
    ax3 = fig.add_subplot(gs[0, 2])
    stream_grp = df.groupby('stream')['compatibility_label'].mean()
    sns.barplot(x=stream_grp.index, y=stream_grp.values * 100, hue=stream_grp.index, ax=ax3, palette='viridis', legend=False)
    ax3.set_title('3. Stream Compatibility Rate (%)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('% Compatible', fontsize=10)
    ax3.set_ylim(0, 100)
    ax3.tick_params(axis='x', rotation=25)

    # 4. Ability Match Boxplot
    ax4 = fig.add_subplot(gs[1, 0])
    sns.boxplot(data=df, x='compatibility_label', y='ability_match_component', hue='compatibility_label', ax=ax4, palette=['#f43f5e', '#10b981'], legend=False)
    ax4.set_title('4. Ability Match by Label', fontsize=12, fontweight='bold')
    ax4.set_xticks([0, 1])
    ax4.set_xticklabels(['Incompatible', 'Compatible'])

    # 5. Interest Match Boxplot
    ax5 = fig.add_subplot(gs[1, 1])
    sns.boxplot(data=df, x='compatibility_label', y='interest_match_component', hue='compatibility_label', ax=ax5, palette=['#f43f5e', '#10b981'], legend=False)
    ax5.set_title('5. Interest Match by Label', fontsize=12, fontweight='bold')
    ax5.set_xticks([0, 1])
    ax5.set_xticklabels(['Incompatible', 'Compatible'])

    # 6. Academic vs Learning Scatter
    ax6 = fig.add_subplot(gs[1, 2])
    sns.scatterplot(
        data=df.sample(2000, random_state=42),
        x='academic_match_component',
        y='learning_match_component',
        hue='compatibility_label',
        palette={0: '#f43f5e', 1: '#10b981'},
        alpha=0.5,
        ax=ax6,
        s=20
    )
    ax6.set_title('6. Academic vs Learning Match', fontsize=12, fontweight='bold')
    ax6.legend(title='Label', loc='upper left')

    fig.suptitle('Career Recommendation System - Comprehensive EDA Executive Dashboard', fontsize=16, fontweight='heavy', y=0.98)

    out_file = OUTPUT_DIR / "07_eda_summary_dashboard.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def main():
    print("=== STARTING COMPREHENSIVE EDA GENERATION ===")
    compat_df, req_df = load_datasets()

    print("\n1. Generating Target and Score Distribution Plot...")
    plot_target_and_score_distribution(compat_df)

    print("\n2. Generating Demographic Analysis Plot...")
    plot_demographic_analysis(compat_df)

    print("\n3. Generating Match Components KDE Distributions...")
    plot_match_components(compat_df)

    print("\n4. Generating Correlation Matrix Heatmap...")
    plot_correlation_heatmap(compat_df)

    print("\n5. Generating Career Domain and Cluster Distribution...")
    plot_career_domains_and_clusters(compat_df)

    print("\n6. Generating Multivariate Interactions Plot...")
    plot_multivariate_interactions(compat_df)

    print("\n7. Generating Executive Summary EDA Dashboard...")
    generate_eda_summary_dashboard(compat_df)

    print(f"\n[SUCCESS] All EDA Figures saved to: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
