# RyanJHamby.github.io

Hugo-based personal portfolio site deployed to GitHub Pages at https://ryanjhamby.dev/ (custom domain; see `static/CNAME`)

## Prerequisites

- [Hugo](https://gohugo.io/) (v0.128.0 or later)
- Git

### Install Hugo

**macOS (via Homebrew):**
```bash
brew install hugo
```

**Linux (via apt):**
```bash
sudo apt-get install hugo
```

**Windows (via Chocolatey):**
```bash
choco install hugo-extended
```

Or download from [gohugo.io/installation](https://gohugo.io/installation/)

## Running Locally

1. Clone the repository with submodules:
```bash
git clone --recurse-submodules https://github.com/ryanjhamby/RyanJHamby.github.io.git
cd RyanJHamby.github.io
```

2. Start the development server:
```bash
hugo server
```

3. Open your browser to `http://localhost:1313/`

The site will auto-rebuild when you make changes to content or configuration.

### Preview Draft Content

To include draft posts in the preview:
```bash
hugo server --buildDrafts
```

## Creating Content

### Add a Blog Post

```bash
hugo new content writing/your-post-title.md
```

This creates a new markdown file in `content/writing/` with default frontmatter.

### Edit Content

Content files are in the `content/` directory:
- `content/_index.md` - Home page
- `content/about.md` - About page
- `content/writing/` - Posts (old `/blog/...` URLs redirect here)

## Publishing

Publishing is automated via GitHub Actions. Simply push changes to the `main` branch:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

GitHub Actions will automatically:
1. Build the Hugo site
2. Deploy to the `gh-pages` branch
3. Update the live site at https://ryanjhamby.dev/

The workflow file is at `.github/workflows/hugo.yml`

## Manual Build

To generate the static site manually:

```bash
hugo
```

This creates the `public/` directory with the built site. The `public/` directory is generated during deployment and not committed to git.

## Project Structure

```
.
├── content/           # Page and post markdown files
├── themes/            # PaperMod theme (git submodule)
├── static/            # Static files (images, etc.)
├── archetypes/        # Content templates
├── public/            # Generated site (not committed)
├── .github/workflows/ # GitHub Actions configuration
└── hugo.toml          # Hugo configuration
```

## Theme

Uses [PaperMod](https://github.com/adityatelange/hugo-PaperMod), a minimal and fast theme for Hugo.

## License

See LICENSE.txt

## How this was built

Design, experiments, and analysis are mine. I used AI coding assistants for
parts of the implementation, tests, and documentation, and reviewed every change.
The 2026-10 site restructure (Writing/Projects/About, custom domain) was done with Claude Code.
The [engineering journal](docs/journal.md) records decisions and dead ends as
they happened, and [`results/`](results/) holds the raw output behind every
number quoted here.
