$OLD_EMAIL = "05640212535@ulife.com.br"
$CORRECT_NAME = "SH1W4"
$CORRECT_EMAIL = "neo.sh1w4@gmail.com"

Write-Host "Reescrevendo historico para corrigir email..."
Write-Host "De: $OLD_EMAIL"
Write-Host "Para: $CORRECT_EMAIL"

# Configura as variaveis de ambiente para o git filter-branch
$env:FILTER_BRANCH_SQUELCH_WARNING = 1

git filter-branch -f --env-filter "
    if [ `"`$GIT_COMMITTER_EMAIL`" = `"$OLD_EMAIL`" ]; then
        export GIT_COMMITTER_NAME=`"$CORRECT_NAME`"
        export GIT_COMMITTER_EMAIL=`"$CORRECT_EMAIL`"
    fi
    if [ `"`$GIT_AUTHOR_EMAIL`" = `"$OLD_EMAIL`" ]; then
        export GIT_AUTHOR_NAME=`"$CORRECT_NAME`"
        export GIT_AUTHOR_EMAIL=`"$CORRECT_EMAIL`"
    fi
" --tag-name-filter cat -- --branches --tags

Write-Host "Historico corrigido. Agora voce precisa forcar o push:"
Write-Host "git push --force"
