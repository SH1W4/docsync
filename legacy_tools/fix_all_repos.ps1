$repos = @(
    "C:\Users\João\Desktop\PROJETOS\00_ECOSYSTEM_COMERCIAL\EDITALSHIELD",
    "C:\Users\João\Desktop\PROJETOS\03_AI_AGENTS\VIREON",
    "C:\Users\João\Desktop\PROJETOS\03_AI_AGENTS\academic-paper-generator",
    "C:\Users\João\Desktop\PROJETOS\03_AI_AGENTS\juridical-innovation-agent",
    "C:\Users\João\Desktop\PROJETOS\03_AI_AGENTS\patent_intelligenc_engine",
    "C:\Users\João\Desktop\PROJETOS\08_PROFILE\sh1w4"
)

$OLD_EMAIL = "05640212535@ulife.com.br"
$CORRECT_NAME = "SH1W4"
$CORRECT_EMAIL = "neo.sh1w4@gmail.com"

foreach ($repo in $repos) {
    Write-Host "---------------------------------------------------"
    Write-Host "Processing Repository: $repo"
    
    if (Test-Path $repo) {
        Set-Location $repo
        
        # Configure Local Git just to be safe
        git config user.email $CORRECT_EMAIL
        git config user.name $CORRECT_NAME
        
        # Stash changes to allow rewrite
        git stash
        
        # Rewrite History
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
        
        # Detect branch name (main or master)
        $branch = git branch --show-current
        Write-Host "Detected branch: $branch"
        
        # Force Push
        Write-Host "Pushing changes to remote..."
        git push --force origin $branch
        
    } else {
        Write-Host "Path not found: $repo" -ForegroundColor Red
    }
}
Write-Host "---------------------------------------------------"
Write-Host "ALL DONE. Check your GitHub Profile."
