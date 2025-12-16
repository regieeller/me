# Minimalist Website

A simple, plain text HTML/CSS website designed for easy updates and maintenance.

## Features

- Clean, minimalist design
- Readable typography with proper spacing
- Responsive layout (works on mobile and desktop)
- No JavaScript dependencies
- Easy to edit and maintain

## File Structure

```
├── index.html    # Main HTML content
├── style.css     # All styling
└── README.md     # This file
```

## How to Update

### Changing Content

Edit `index.html` to update your content:
- Update the `<title>` tag to change the browser tab title
- Modify text inside `<p>` tags for paragraphs
- Change headings in `<h1>` and `<h2>` tags
- Update the email address in the contact section
- Add your name in the footer

### Adding New Sections

Copy this template and paste it before the `<footer>` tag:

```html
<section>
    <h2>New Section Title</h2>
    <p>Your content here.</p>
</section>
```

### Customizing Colors

Edit `style.css` to change colors:
- `color: #333` - Main text color
- `background-color: #fff` - Page background
- `color: #0066cc` - Link color
- `color: #666` - Footer text color

### Adjusting Font Size

In `style.css`, change:
- `font-size: 18px` in `body` for base text size
- Font sizes in `h1` and `h2` for heading sizes

## Viewing Locally

Simply open `index.html` in your web browser.

## Deploying

Upload `index.html` and `style.css` to any web hosting service:
- GitHub Pages
- Netlify
- Vercel
- Traditional web hosting

No build process required!
