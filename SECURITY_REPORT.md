# Отчет по анализу исходного кода Ryuzaki/CyberHacks

В ходе глубокого статического и ручного анализа кодовой базы были выявлены следующие архитектурные уязвимости и потенциальные баги. Зловредного кода (бэкдоров, стилеров, RCE) **не обнаружено**, однако присутствуют критические ошибки логики, способные привести к крашам (DDoS) или утечкам.

---

### 1. Утечка сессий (Открытое хранение аккаунтов)
**Файл:** `src/main/java/ru/ryuzaki/gui/AltManagerScreen.java`
**Строки:** ~100-117
**Описание проблемы:**
Методы `loadAccounts()` и `saveAccounts()` сохраняют и читают список аккаунтов (и, возможно, токены сессий в будущем) в файле `ryuzaki/alts.json` в открытом виде (Plain Text). Любой вредоносный мод или скрипт в системе может прочитать этот файл и украсть лицензионные аккаунты.

**Как пофиксить:**
Использовать симметричное шифрование (например, AES) для файла `alts.json`, используя ключ, уникальный для машины пользователя (например, хэш от MAC-адреса или свойств железа), либо использовать стандартную Windows Data Protection API (DPAPI) / Keychain на macOS.

```java
// Пример простого шифрования:
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

// Зашифровать строку перед записью в alts.json
public static String encrypt(String value, String key) throws Exception {
    SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), "AES");
    Cipher cipher = Cipher.getInstance("AES");
    cipher.init(Cipher.ENCRYPT_MODE, keySpec);
    return Base64.getEncoder().encodeToString(cipher.doFinal(value.getBytes()));
}
```

---

### 2. Зависание потоков (Thread Starvation / Blocking I/O) в парсере GIF
**Файл:** `src/main/java/ru/ryuzaki/ui/components/gif/GifDecoder.java`
**Строки:** ~14-20
**Описание проблемы:**
При чтении GIF по URL используется `new BufferedInputStream(url.openStream());` без установки таймаутов на подключение и чтение. Если целевой сервер медленный или не отвечает (например, специально настроен злоумышленником), поток зависнет навсегда (infinite block). Если это происходит в основном потоке рендера Minecraft — игра намертво зависнет.

**Как пофиксить:**
Использовать `URLConnection` с явным указанием `ConnectTimeout` и `ReadTimeout`.

```java
<<<<<<< SEARCH
            if (name.contains("file:") || name.indexOf(":/") > 0) {
                URL url = new URL(name);
                this.in = new BufferedInputStream(url.openStream());
            } else {
=======
            if (name.contains("file:") || name.indexOf(":/") > 0) {
                URL url = new URL(name);
                java.net.URLConnection conn = url.openConnection();
                conn.setConnectTimeout(5000); // 5 секунд
                conn.setReadTimeout(5000);
                this.in = new BufferedInputStream(conn.getInputStream());
            } else {
>>>>>>> REPLACE
```

---

### 3. Утечки процессов (Zombie Processes)
**Файл:** `src/main/java/ru/ryuzaki/util/MediaUtil.java` (и `MusicPlayerModule.java`)
**Строки:** ~147
**Описание проблемы:**
Для получения названия трека создается процесс PowerShell через `ProcessBuilder`. Процесс запускается, и программа ждет его завершения `proc.waitFor()`. Если скрипт PowerShell зависнет внутри (например, из-за конфликта Windows API), процесс так и останется висеть в памяти, а поскольку это происходит в планировщике `exec.scheduleAtFixedRate`, это приведет к экспоненциальному росту зомби-процессов `powershell.exe`, что вызовет лаги компьютера (Memory/CPU Leak).

**Как пофиксить:**
Обязательно вызывать `proc.destroyForcibly()` в блоке `finally`.

```java
<<<<<<< SEARCH
            proc.waitFor(2, TimeUnit.SECONDS);
            proc.destroyForcibly();
            if (out == null || out.equals("NONE") || out.isBlank()) {
=======
            proc.waitFor(2, TimeUnit.SECONDS);
            if (out == null || out.equals("NONE") || out.isBlank()) {
>>>>>>> REPLACE
```
*Примечание: В коде уже есть `destroyForcibly`, но он может быть не вызван, если `waitFor` бросит `InterruptedException` (которое перехватывается общим `catch (Exception)` ниже, оставляя процесс живым). Рекомендуется обернуть вызов `destroy` в `finally`.*

---

### 4. Неконтролируемый рост очереди пакетов
**Файл:** `src/main/java/com/professor/cyberhacks/PacketBuffer.java`
**Строки:** ~35
**Описание проблемы:**
Хотя присутствует ограничение `MAX_QUEUE_SIZE = 64`, метод `add` добавляет новые пакеты с помощью `QUEUE.offer()`. Если `poll()` вызывается реже, чем `add()` (например, лаги сети или низкий TPS сервера), очередь все равно не превысит 64 элемента, **но** старые пакеты будут просто отбрасываться, что приведет к рассинхронизации состояния клиента и сервера (Desync), фантомным блокам и кикам за "Bad Packets".

**Как пофиксить:**
Вместо отбрасывания пакетов, если буфер переполнен, лучше отправлять старые пакеты принудительно (flush), освобождая место, либо динамически увеличивать буфер до определенного безопасного предела (например, 1000).

```java
<<<<<<< SEARCH
    public static void add(Packet packet) {
        if (QUEUE.size() >= MAX_QUEUE_SIZE) {
            QUEUE.poll();
        }
=======
    public static void add(Packet packet) {
        var nh = MC.networkHandler();
        while (QUEUE.size() >= MAX_QUEUE_SIZE) {
            DelayedPacket dropped = QUEUE.poll();
            if (nh != null && dropped != null) {
                nh.sendPacket(dropped.packet());
            }
        }
>>>>>>> REPLACE
```
