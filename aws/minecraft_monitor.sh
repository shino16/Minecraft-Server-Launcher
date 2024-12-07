while true
do
    sleep 600
    cat /var/log/syslog | tac | sed '/Started minecraft\.service - Minecraft Server/q' | tac > minecraft_syslog.txt
    connected_count=`grep -oi "Player connected" minecraft_syslog.txt | wc -l`
    disconnected_count=`grep -oi "Player disconnected" minecraft_syslog.txt | wc -l`

    if [ $connected_count -eq 0 ]; then
        continue
    fi

    if [ $connected_count -eq $disconnected_count ]; then
        shutdown
        return 0
    fi
done
