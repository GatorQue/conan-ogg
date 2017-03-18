#include <stdio.h>
#include <string.h>

#include <ogg/ogg.h>

int main(int argc, char **argv)
{
    ogg_sync_state sync_state;
    sync_state.data = NULL;
    sync_state.storage = 1;
    sync_state.fill = 1;
    sync_state.returned = 1;
    sync_state.unsynced = 1;
    sync_state.headerbytes = 0;
    sync_state.bodybytes = 0;

    return 0;
}
