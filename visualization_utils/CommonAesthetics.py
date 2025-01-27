def apply_common_aesthetics(fig, title_color = "black"):
    fig.update_layout(
        plot_bgcolor="#f8f8f8",
        paper_bgcolor="#ffffff",
        font=dict(size=16, color="darkblue"),
        title=dict(font=dict(size=20, color=title_color))
    )
    return fig