#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <openssl/sha.h>

#define C_RESET   "\033[0m"
#define C_RED     "\033[31m"
#define C_GREEN   "\033[32m"
#define C_CYAN    "\033[36m"
#define C_MAGENTA "\033[35m"
#define C_YELLOW  "\033[33m"

void log_line(const char *level, const char *color, const char *msg) {
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    char buf[20];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", t);
    printf("%s[%s] %-7s:%s %s\n", color, buf, level, C_RESET, msg);
}

void spinner(int cycles) {
    const char spin[] = "|/-\\";
    for (int i = 0; i < cycles; i++) {
        putchar(spin[i % 4]);
        usleep(50000);
        putchar('\b');
    }
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);

    char user[32], pass[128];
    unsigned char hash[SHA256_DIGEST_LENGTH];
    char hexhash[SHA256_DIGEST_LENGTH*2 + 1];
    const char *admin_hash = "7fa25ad1554a3d3436f93d5e696cba801a7a82bb7a12242f686e7885d93b50d4";

    printf(C_MAGENTA
        "\n"
        "████████╗ █████╗ ███╗   ███╗██╗   ██╗ ██████╗████████╗███████╗ \n"
        "╚══██╔══╝██╔══██╗████╗ ████║██║   ██║██╔════╝╚══██╔══╝██╔════╝ \n"
        "   ██║   ███████║██╔████╔██║██║   ██║██║        ██║   █████╗   \n"
        "   ██║   ██╔══██║██║╚██╔╝██║██║   ██║██║        ██║   ██╔══╝   \n"
        "   ██║   ██║  ██║██║ ╚═╝ ██║╚██████╔╝╚██████╗   ██║   ██║      \n"
        "   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝   ╚═╝   ╚═╝      \n"
        "                                                               \n"
        "                  ██╗   ██╗██████╗ ███╗   ██╗                  \n"
        "                  ██║   ██║██╔══██╗████╗  ██║                  \n"
        "                  ██║   ██║██████╔╝██╔██╗ ██║                  \n"
        "                  ╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║                  \n"
        "                ██╗╚████╔╝ ██║     ██║ ╚████║██╗               \n"
        "                ╚═╝ ╚═══╝  ╚═╝     ╚═╝  ╚═══╝╚═╝               \n"
        "                                                               \n"
        "            ██╗      ██████╗  ██████╗ ██╗███╗   ██╗            \n"
        "            ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║            \n"
        "            ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║            \n"
        "            ██║     ██║   ██║██║   ██║██║██║╚██╗██║            \n"
        "            ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║            \n"
        "            ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝            \n"
        "             T A M U C T F   V P N   A C C E S S\n\n"
        C_RESET
    );

    log_line("INFO", C_CYAN, "Starting VPN client...");
    spinner(20);
    log_line("DEBUG", C_CYAN, "Loading VPN modules.");

    printf(C_YELLOW ">> " C_RESET "VPN Username: ");
    if (!fgets(user, sizeof(user), stdin)) {
        log_line("ERROR", C_RED, "Failed to read username.");
        return 1;
    }
    user[strcspn(user, "\n")] = 0;
    log_line("DEBUG", C_CYAN, "Username entered.");

    printf(C_YELLOW ">> " C_RESET "VPN Password: ");
    if (!fgets(pass, sizeof(pass), stdin)) {
        log_line("ERROR", C_RED, "Failed to read password.");
        return 1;
    }
    pass[strcspn(pass, "\n")] = 0;
    log_line("DEBUG", C_CYAN, "Password captured.\n");

    if (strcmp(user, "tamu_admin") != 0) {
        log_line("WARN", C_RED, "Invalid VPN user.");
        printf("\n" C_RED "*** CONNECTION REFUSED ***" C_RESET "\n");
        return 1;
    }
    log_line("INFO", C_GREEN, "VPN user verified.");

    log_line("DEBUG", C_CYAN, "Hashing credentials...");
    spinner(15);
    SHA256((unsigned char*)pass, strlen(pass), hash);
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(hexhash + i*2, "%02x", hash[i]);
    }
    hexhash[SHA256_DIGEST_LENGTH*2] = 0;
    log_line("DEBUG", C_CYAN, "Hash computed.");

    if (strcmp(hexhash, admin_hash) == 0) {
        log_line("SUCCESS", C_GREEN, "Password match confirmed.");
        printf("\n" C_GREEN "*** VPN TUNNEL ESTABLISHED ***" C_RESET "\n");
        printf(C_MAGENTA "Connecting to TAMUCTF database");
        fflush(stdout);
        for (int i = 0; i < 3; i++) {
            spinner(10);
            printf(".");
            fflush(stdout);
        }
        printf("\n\n");

        char flag[128];
        FILE *f = fopen("flag.txt", "r");
        if (!f) {
            log_line("ERROR", C_RED, "Unable to access flags database.");
            perror("   [SYSTEM]");
            return 1;
        }
        while (fgets(flag, sizeof(flag), f)) {
            printf(C_YELLOW ">> %s" C_RESET, flag);
        }
        printf("\n\n");
        fclose(f);

        log_line("INFO", C_CYAN, "All flags exfiltrated. Disconnecting.");
    } else {
        log_line("WARN", C_RED, "Password mismatch.");
        printf("\n" C_RED "*** VPN AUTHENTICATION FAILED ***" C_RESET "\n");
        log_line("INFO", C_CYAN, "Session terminated.");
    }

    return 0;
}