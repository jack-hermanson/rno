function themeSwitcher() {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

    return {
        themes: ["light", "dark"],
        currentTheme: localStorage.getItem("theme") || (prefersDark.matches ? "dark" : "light"),

        setTheme(newTheme) {
            this.currentTheme = newTheme;
            localStorage.setItem("theme", newTheme);
            document.documentElement.setAttribute("data-bs-theme", newTheme);
        }
    };
}

document.addEventListener("DOMContentLoaded", () => {
    const themeSwitcherInstance = themeSwitcher();

    // Update theme when system preference changes
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
        if (!localStorage.getItem("theme")) {
            themeSwitcherInstance.setTheme(e.matches ? "dark" : "light");
        }
    });
});