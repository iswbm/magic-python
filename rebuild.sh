cat << EOF >/usr/local/lib/python3.10/site-packages/sphinx_rtd_theme/comments.html
<comments>
  <script src="https://utteranc.es/client.js"
    repo="iswbm/magic-python"
    issue-term="pathname"
    theme="github-light"
    crossorigin="anonymous"
    async>
  </script>
</comments>
EOF

rm -rf build/ && sphinx-multiversion source build/html && cp -rf build/html/master/* build/html/
