import path from 'path';
import { PortablePython } from '@bjia56/portable-python';
import { ScryptedDeviceBase } from '@scrypted/sdk';

class PythonRuntime extends ScryptedDeviceBase {
    python: PortablePython

    constructor(nativeId?: string) {
        super(nativeId);
        this.python = new PortablePython("3.9", path.join(process.env.SCRYPTED_PLUGIN_VOLUME, 'python'));
        this.install()
    }

    async install() {
        await this.python.install();
        this.console.log(`Python installed to path: ${this.python.executablePath}`);
    }
}

export default PythonRuntime;
