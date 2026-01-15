module.exports = {
    apps: [{
      name: 'blog-frontend',
      script: 'node_modules/next/dist/bin/next',
      args: 'start',
      cwd: '/home/blog/PersonalBlobDynamic/frontend',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    }]
  };