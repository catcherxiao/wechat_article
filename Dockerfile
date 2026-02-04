FROM nginx:alpine

# Copy the static HTML file
COPY wechat_workflow.html /usr/share/nginx/html/index.html

# Copy the prompts directory so the web page can load them
COPY prompts /usr/share/nginx/html/prompts

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
